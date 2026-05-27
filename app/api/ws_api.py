from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.core.connection_manager import ConnectionManager
from app.core.security import verify_token
from app.services.auth_service import get_user_by_id
from app.core.database import SessionLocal

from app.models.assembly import Assembly
from app.models.motion import Motion
from app.models.vote import Vote

from app.enums.system_enums import (
    AssemblyStatus,
    MotionStatus,
    UserRole
)

import uuid
import json

router = APIRouter()
manager = ConnectionManager()


@router.websocket("/ws/{assembly_id}")
async def websocket_endpoint(websocket: WebSocket, assembly_id: str):

    token = websocket.query_params.get("token")

    if not token:
        await websocket.close()
        return

    db = SessionLocal()

    try:
        # =========================
        # 🔒 VALIDAR ASSEMBLY ID (ANTES DE TODO)
        # =========================
        try:
            assembly_uuid = uuid.UUID(assembly_id)
        except:
            await websocket.close()
            return

        # =========================
        # 🔐 VALIDAR TOKEN
        # =========================
        payload = verify_token(token)
        if not payload:
            await websocket.close()
            return

        user_id = payload.get("sub")
        user = get_user_by_id(db, uuid.UUID(user_id))

        if not user:
            await websocket.close()
            return

        # =========================
        # 🔌 CONECTAR
        # =========================
        await manager.connect(assembly_id, websocket, user)

        # =========================
        # 📡 PRESENCE INICIAL
        # =========================
        await manager.broadcast(
            assembly_id,
            {
                "type": "presence",
                "users": manager.get_users(assembly_id),
                "count": manager.get_count(assembly_id),
                "quorum": manager.get_quorum(assembly_id)
            }
        )

        # =========================
        # 🔁 LOOP PRINCIPAL
        # =========================
        while True:

            raw_data = await websocket.receive_text()

            try:
                data = json.loads(raw_data)
            except:
                continue

            msg_type = data.get("type")

            # =========================
            # 💬 CHAT
            # =========================
            if msg_type == "message":

                await manager.broadcast(
                    assembly_id,
                    {
                        "type": "message",
                        "user": user.full_name,
                        "data": data.get("data")
                    }
                )

            # =========================
            # 🟢 INICIAR VOTACIÓN
            # =========================
            elif msg_type == "start_motion":

                if user.role != UserRole.ADMIN:
                    await websocket.send_json({
                        "type": "error",
                        "message": "Solo ADMIN"
                    })
                    continue

                try:
                    motion_id = uuid.UUID(data.get("motion_id"))
                except:
                    await websocket.send_json({
                        "type": "error",
                        "message": "motion_id inválido"
                    })
                    continue

                motion = db.query(Motion).filter(
                    Motion.id == motion_id
                ).first()

                if not motion:
                    continue

                # activar moción
                motion.status = MotionStatus.VOTING

                # activar asamblea
                assembly = db.query(Assembly).filter(
                    Assembly.id == assembly_uuid
                ).first()

                if assembly:
                    assembly.status = AssemblyStatus.VOTING

                db.commit()

                await manager.broadcast(
                    assembly_id,
                    {
                        "type": "motion_started",
                        "motion_id": str(motion_id)
                    }
                )

            # =========================
            # 🔴 CERRAR VOTACIÓN
            # =========================
            elif msg_type == "close_motion":

                if user.role != UserRole.ADMIN:
                    await websocket.send_json({
                        "type": "error",
                        "message": "Solo ADMIN"
                    })
                    continue

                try:
                    motion_id = uuid.UUID(data.get("motion_id"))
                except:
                    await websocket.send_json({
                        "type": "error",
                        "message": "motion_id inválido"
                    })
                    continue

                motion = db.query(Motion).filter(
                    Motion.id == motion_id
                ).first()

                if not motion:
                    continue

                # =========================
                # 📊 RESULTADOS
                # =========================
                votes = db.query(Vote).filter(
                    Vote.motion_id == motion_id
                ).all()

                results = {"YES": 0, "NO": 0, "ABSTAIN": 0}
                votes_detail = []

                for v in votes:

                    val = v.vote_value.upper()

                    if val in results:
                        results[val] += 1

                    votes_detail.append({
                        "user_id": str(v.user_id),
                        "vote": val,
                        "party": getattr(v.user, "party", "SIN_GRUPO")
                    })

                # =========================
                # 🧠 DECISIÓN FINAL
                # =========================
                if results["YES"] > results["NO"]:
                    motion.status = MotionStatus.APPROVED
                else:
                    motion.status = MotionStatus.REJECTED

                # devolver asamblea a estado normal
                assembly = db.query(Assembly).filter(
                    Assembly.id == assembly_uuid
                ).first()

                if assembly:
                    assembly.status = AssemblyStatus.OPEN

                db.commit()

                await manager.broadcast(
                    assembly_id,
                    {
                        "type": "motion_closed",
                        "motion_id": str(motion_id),
                        "results": results,
                        "votes_detail": votes_detail,
                        "quorum": manager.get_quorum(assembly_id)
                    }
                )

            # =========================
            # 🗳️ VOTAR
            # =========================
            elif msg_type == "vote":

                try:
                    motion_id = uuid.UUID(data.get("motion_id"))
                except:
                    await websocket.send_json({
                        "type": "error",
                        "message": "motion_id inválido"
                    })
                    continue

                vote_value = data.get("vote")

                if not vote_value:
                    await websocket.send_json({
                        "type": "error",
                        "message": "Voto vacío"
                    })
                    continue

                vote_value = vote_value.upper()

                if vote_value not in ["YES", "NO", "ABSTAIN"]:
                    await websocket.send_json({
                        "type": "error",
                        "message": "Voto inválido"
                    })
                    continue

                # validar asamblea
                assembly = db.query(Assembly).filter(
                    Assembly.id == assembly_uuid
                ).first()

                if not assembly or assembly.status != AssemblyStatus.VOTING:
                    await websocket.send_json({
                        "type": "error",
                        "message": "Asamblea no en votación"
                    })
                    continue

                # validar moción
                motion = db.query(Motion).filter(
                    Motion.id == motion_id
                ).first()

                if not motion or motion.status != MotionStatus.VOTING:
                    await websocket.send_json({
                        "type": "error",
                        "message": "Moción no activa"
                    })
                    continue

                # 🔒 evitar condición de carrera
                db.refresh(motion)
                if motion.status != MotionStatus.VOTING:
                    await websocket.send_json({
                        "type": "error",
                        "message": "Votación cerrada"
                    })
                    continue

                # validar rol
                if user.role not in [
                    UserRole.ASSEMBLY_MEMBER,
                    UserRole.ADMIN
                ]:
                    await websocket.send_json({
                        "type": "error",
                        "message": "No autorizado"
                    })
                    continue

                # evitar doble voto
                existing = db.query(Vote).filter(
                    Vote.motion_id == motion_id,
                    Vote.user_id == user.id
                ).first()

                if existing:
                    await websocket.send_json({
                        "type": "error",
                        "message": "Ya votaste"
                    })
                    continue

                # guardar voto
                new_vote = Vote(
                    motion_id=motion_id,
                    user_id=user.id,
                    vote_value=vote_value
                )

                db.add(new_vote)
                db.commit()

                # =========================
                # 📊 RESULTADOS EN VIVO
                # =========================
                votes = db.query(Vote).filter(
                    Vote.motion_id == motion_id
                ).all()

                results = {"YES": 0, "NO": 0, "ABSTAIN": 0}
                votes_detail = []

                for v in votes:

                    val = v.vote_value.upper()

                    if val in results:
                        results[val] += 1

                    votes_detail.append({
                        "user_id": str(v.user_id),
                        "vote": val,
                        "party": getattr(v.user, "party", "SIN_GRUPO")
                    })

                await manager.broadcast(
                    assembly_id,
                    {
                        "type": "vote_update",
                        "motion_id": str(motion_id),
                        "results": results,
                        "votes_detail": votes_detail,
                        "quorum": manager.get_quorum(assembly_id)
                    }
                )

    except WebSocketDisconnect:

        manager.disconnect(assembly_id, websocket)

        await manager.broadcast(
            assembly_id,
            {
                "type": "presence",
                "users": manager.get_users(assembly_id),
                "count": manager.get_count(assembly_id),
                "quorum": manager.get_quorum(assembly_id)
            }
        )

    except Exception as e:
        print("ERROR WS:", e)
        manager.disconnect(assembly_id, websocket)
        await websocket.close()

    finally:
        db.close()