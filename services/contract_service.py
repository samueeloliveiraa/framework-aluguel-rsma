"""
MICROSSERVIÇO: ContractService (Serviço de Gestão de Contratos de Locação)
Responsabilidade: Criação, assinatura e ciclo de vida dos contratos de aluguel.
"""
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import uuid
from framework_aluguel.components.notification_component import NotificationComponent
from framework_aluguel.gateway.event_bus import bus


class ContractService:
    """Microsserviço responsável pelos contratos de locação."""

    def __init__(self, property_service=None):
        self.property_service = property_service
        self.notification_comp = NotificationComponent()
        self._contracts: Dict[str, Dict[str, Any]] = {}

    def set_property_service(self, ps):
        self.property_service = ps

    def criar_proposta(self, imovel_id: str, inquilino_nome: str, inquilino_email: str, renda_declarada: float, duracao_meses: int = 12, garantia: str = "Caução") -> Dict[str, Any]:
        """Gera uma minuta de proposta de locação."""
        imovel = None
        if self.property_service:
            imovel = self.property_service.obter_imovel(imovel_id)

        if not imovel:
            raise ValueError(f"Imóvel {imovel_id} não encontrado ou indisponível.")

        contrato_id = f"CTR-{str(uuid.uuid4())[:6].upper()}"
        custos = imovel["custos"]
        data_inicio = datetime.now()
        data_fim = data_inicio + timedelta(days=duracao_meses * 30)

        contrato = {
            "contrato_id": contrato_id,
            "imovel_id": imovel_id,
            "imovel_titulo": imovel["titulo"],
            "tipo_imovel": imovel["tipo"],
            "inquilino_nome": inquilino_nome,
            "inquilino_email": inquilino_email,
            "renda_declarada": renda_declarada,
            "valor_aluguel": custos["aluguel_base"],
            "valor_total_mensal": custos["total_mensal"],
            "caucao_exigida": custos["caucao_sugerida"],
            "garantia_adotada": garantia,
            "duracao_meses": duracao_meses,
            "data_inicio": data_inicio.strftime("%Y-%m-%d"),
            "data_fim": data_fim.strftime("%Y-%m-%d"),
            "status": "PROPOSTA_EMITIDA"  # PROPOSTA_EMITIDA -> ATIVO -> FINALIZADO
        }

        self._contracts[contrato_id] = contrato

        # Notifica as partes envolvidas através do NotificationComponent
        self.notification_comp.notificar(
            canal="EMAIL",
            destinatario=inquilino_email,
            assunto=f"Proposta de Locação #{contrato_id} - {imovel['titulo']}",
            mensagem=f"Prezado(a) {inquilino_nome}, sua proposta de R$ {custos['total_mensal']}/mês foi gerada."
        )

        bus.log_call(
            origem="Consumer/AIAgent",
            destino="ContractService",
            operacao="criar_proposta",
            payload={"imovel_id": imovel_id, "inquilino": inquilino_nome},
            resposta=f"Contrato {contrato_id} criado"
        )

        return contrato

    def assinar_contrato(self, contrato_id: str) -> Dict[str, Any]:
        """Formaliza e ativa o contrato de aluguel."""
        contrato = self._contracts.get(contrato_id)
        if not contrato:
            raise ValueError(f"Contrato {contrato_id} não encontrado.")

        contrato["status"] = "ATIVO"
        contrato["data_assinatura"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Atualiza status do imóvel no PropertyService para ALUGADO
        if self.property_service:
            self.property_service.atualizar_status(contrato["imovel_id"], "ALUGADO")

        self.notification_comp.notificar(
            canal="EMAIL",
            destinatario=contrato["inquilino_email"],
            assunto=f"Parabéns! Contrato #{contrato_id} Ativado!",
            mensagem=f"Seu contrato para {contrato['imovel_titulo']} está oficialmente assinado e vigente!"
        )

        bus.log_call(
            origem="Consumer",
            destino="ContractService",
            operacao="assinar_contrato",
            payload={"contrato_id": contrato_id},
            resposta="Status alterado para ATIVO"
        )
        return contrato

    def listar_contratos(self) -> List[Dict[str, Any]]:
        return list(self._contracts.values())
