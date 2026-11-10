"""
MICROSSERVIÇO: PropertyService (Serviço de Gestão de Imóveis)
Responsabilidade: Catálogo, disponibilidade e especificações de Apartamentos e Casas.
Banco de Dados próprio (autonomia de dados no microsserviço).
"""
from typing import List, Dict, Any, Optional
from framework_aluguel.components.pricing_component import PricingCalculatorComponent
from framework_aluguel.gateway.event_bus import bus


class PropertyService:
    """Microsserviço de Catálogo de Imóveis."""

    def __init__(self):
        self.pricing_comp = PricingCalculatorComponent()
        # Base de dados em memória do serviço (bounded context de Imóveis)
        self._properties: Dict[str, Dict[str, Any]] = {
            "APT-101": {
                "id": "APT-101",
                "tipo": "Apartamento",
                "titulo": "Apto Moderno no Centro",
                "bairro": "Centro",
                "quartos": 2,
                "banheiros": 1,
                "vagas": 1,
                "aceita_pets": True,
                "aluguel_base": 2200.0,
                "condominio": 450.0,
                "iptu": 110.0,
                "status": "DISPONIVEL",
                "descricao": "Apartamento ensolarado, próximo ao metrô e comércio. Varanda gourmet."
            },
            "APT-202": {
                "id": "APT-202",
                "tipo": "Apartamento",
                "titulo": "Studio Compacto Universitário",
                "bairro": "Universitário",
                "quartos": 1,
                "banheiros": 1,
                "vagas": 0,
                "aceita_pets": False,
                "aluguel_base": 1400.0,
                "condominio": 280.0,
                "iptu": 60.0,
                "status": "DISPONIVEL",
                "descricao": "Ideal para estudantes ou solteiros. Mobiliado com armários embutidos."
            },
            "CASA-301": {
                "id": "CASA-301",
                "tipo": "Casa",
                "titulo": "Casa Ampla com Quintal e Churrasqueira",
                "bairro": "Jardim das Flores",
                "quartos": 3,
                "banheiros": 2,
                "vagas": 2,
                "aceita_pets": True,
                "aluguel_base": 3600.0,
                "condominio": 0.0,
                "iptu": 180.0,
                "status": "DISPONIVEL",
                "descricao": "Excelente casa térrea com quintal gramado grande, canil e área gourmet."
            },
            "CASA-402": {
                "id": "CASA-402",
                "tipo": "Casa",
                "titulo": "Sobrado em Condomínio Fechado",
                "bairro": "Parque Verde",
                "quartos": 4,
                "banheiros": 3,
                "vagas": 3,
                "aceita_pets": True,
                "aluguel_base": 5200.0,
                "condominio": 600.0,
                "iptu": 320.0,
                "status": "DISPONIVEL",
                "descricao": "Casa de alto padrão com segurança 24h, piscina no condomínio e playground."
            },
            "APT-505": {
                "id": "APT-505",
                "tipo": "Apartamento",
                "titulo": "Cobertura Duplex com Vista Panorâmica",
                "bairro": "Bela Vista",
                "quartos": 3,
                "banheiros": 3,
                "vagas": 2,
                "aceita_pets": True,
                "aluguel_base": 6500.0,
                "condominio": 1100.0,
                "iptu": 450.0,
                "status": "DISPONIVEL",
                "descricao": "Cobertura com jacuzzi privada, vista da cidade e excelente acabamento."
            }
        }

    def listar_imoveis(self, tipo: Optional[str] = None, max_aluguel: Optional[float] = None, aceita_pets: Optional[bool] = None, quartos_min: Optional[int] = None) -> List[Dict[str, Any]]:
        """Consulta o catálogo aplicando filtros de negócio e enriquecendo com o componente de preços."""
        resultados = []
        for prop in self._properties.values():
            if prop["status"] != "DISPONIVEL":
                continue
            if tipo and tipo != "Todos" and prop["tipo"].lower() != tipo.lower():
                continue
            if quartos_min and prop["quartos"] < quartos_min:
                continue
            if aceita_pets is not None and aceita_pets and not prop["aceita_pets"]:
                continue

            # Usa o componente de precificação para calcular total estimado
            pricing = self.pricing_comp.calcular_custos(
                aluguel_base=prop["aluguel_base"],
                condominio=prop["condominio"],
                iptu=prop["iptu"]
            )

            if max_aluguel and pricing.total_mensal > max_aluguel:
                continue

            item = dict(prop)
            item["custos"] = self.pricing_comp.to_dict(pricing)
            resultados.append(item)

        bus.log_call(
            origem="Consumer",
            destino="PropertyService",
            operacao="listar_imoveis",
            payload={"tipo": tipo, "max_aluguel": max_aluguel, "aceita_pets": aceita_pets, "quartos_min": quartos_min},
            resposta=f"{len(resultados)} imóveis encontrados"
        )
        return resultados

    def obter_imovel(self, imovel_id: str) -> Optional[Dict[str, Any]]:
        prop = self._properties.get(imovel_id)
        if not prop:
            return None
        res = dict(prop)
        pricing = self.pricing_comp.calcular_custos(prop["aluguel_base"], prop["condominio"], prop["iptu"])
        res["custos"] = self.pricing_comp.to_dict(pricing)
        bus.log_call("Consumer", "PropertyService", "obter_imovel", {"id": imovel_id}, res["titulo"])
        return res

    def atualizar_status(self, imovel_id: str, novo_status: str) -> bool:
        if imovel_id in self._properties:
            self._properties[imovel_id]["status"] = novo_status
            bus.log_call("Service", "PropertyService", "atualizar_status", {"id": imovel_id, "status": novo_status}, "OK")
            return True
        return False
