"""Quem pode o quê.

O TAP define dois perfis — Administrador e Operador — e eles não são
decorativos: o operador de campo lança ordenha, peso e vacinação, mas não
mexe em cadastro de raça, espécie ou usuário.

Os papéis são Grupos do Django (`auth.Group`), e não um campo booleano, por
dois motivos: o Django Admin já sabe editar grupo, então incluir alguém no
perfil não exige tela nova; e um terceiro perfil (veterinário, por exemplo)
entra sem migração de banco.
"""

from rest_framework.permissions import SAFE_METHODS, BasePermission

ADMINISTRADOR = "Administrador"
OPERADOR = "Operador"


def papel_de(user) -> str:
    """O papel do usuário, em uma palavra.

    `is_superuser` continua valendo como Administrador para não trancar
    ninguém para fora ao aplicar isto num banco que já existe — os usuários
    de hoje foram criados antes dos grupos existirem.
    """
    if not user or not user.is_authenticated:
        return ""
    if user.is_superuser or user.groups.filter(name=ADMINISTRADOR).exists():
        return ADMINISTRADOR
    if user.groups.filter(name=OPERADOR).exists():
        return OPERADOR
    return OPERADOR


class EhAdministrador(BasePermission):
    """Só Administrador passa."""

    message = "Esta ação é restrita ao Administrador."

    def has_permission(self, request, view):
        return papel_de(request.user) == ADMINISTRADOR


class AdministradorEscreveOperadorLe(BasePermission):
    """Operador consulta, Administrador altera.

    Para os cadastros estruturais — espécie, raça, quadrante, vacina, tipo de
    movimentação. O operador precisa LER esses dados para preencher um
    lançamento (escolher a vacina que aplicou), mas quem define o catálogo é
    o administrador. Sem isso, um erro de digitação no campo vira raça nova.
    """

    message = "Apenas o Administrador pode alterar este cadastro."

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)
        return papel_de(request.user) == ADMINISTRADOR
