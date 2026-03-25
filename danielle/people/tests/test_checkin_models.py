import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone
from people.models import Person, Checkin, Checkout, HomeServices

# marca todos os testes neste módulo para usar o banco de dados do Django
pytestmark = pytest.mark.django_db


@pytest.fixture  # cria a pessoa e retorna o objeto person para testes
def create_person():
    """Fixture para criar uma pessoa para os testes."""
    return Person.objects.create(
        name="Teste Pessoa",
        cpf="12345678901",
        born_date="1990-01-01",
        gender="M",
        private_phone="987654321",
        email="teste@example.com",
        address_line_1="Rua Teste, 123",
        city="SAO PAULO",
        state="SP",
        postal_code="01000000",
    )


def test_checkin_block_multiple_active_checkins(create_person):
    """
    testa se o sistema bloqueia a criacao de multiplos check-ins ativos
    para a mesma pessoa.
    """
    person = create_person

    # 1. cria um check-in ativo para a pessoa
    Checkin.objects.create(person=person, reason="patient", active=True)

    # 2. tenta criar um segundo check-in ativo para a mesma pessoa
    with pytest.raises(ValidationError) as excinfo:
        new_checkin = Checkin(person=person, reason="patient", active=True)
        new_checkin.full_clean()

    # 3. verifica se a mensagem de erro esperada foi retornada
    assert "Esta pessoa já possui um check-in ativo." in str(
        excinfo.value.message_dict["person"]
    )


def test_checkout_changes_checkin_to_inactive(create_person):
    """
    testa se a melhoria 2 está funcionando: ao salvar um Checkout,
    o Checkin associado deve ser alterado para active=False automaticamente.
    """
    person = create_person

    # 1. cria um check-in ativo
    checkin = Checkin.objects.create(person=person, reason="patient", active=True)
    assert checkin.active is True  # garante o estado inicial

    # 2. cria o checkout para esse check-in
    Checkout.objects.create(checkin=checkin)

    # 3. atualiza o objeto checkin buscando as informações mais recentes do banco de dados
    checkin.refresh_from_db()

    # 4. verifica se o Check-in agora está inativo (False)
    assert checkin.active is False


def test_checkin_block_for_deceased_person(create_person):
    """
    testa se a Melhoria 3 esta funcionando: bloqueia check-in
    se a pessoa possui data de óbito registrada.
    """
    person = create_person

    # 1. registra a data de óbito para a pessoa e salva
    person.death_date = "2023-01-01"
    person.save()

    # 2. tenta criar um check-in para a pessoa em óbito
    with pytest.raises(ValidationError) as excinfo:
        new_checkin = Checkin(person=person, reason="patient", active=True)
        new_checkin.full_clean()

    # 3. verifica se a mensagem de erro esperada foi retornada
    assert "Não é possível realizar check-in para um paciente em óbito." in str(
        excinfo.value.message_dict["person"]
    )


def test_home_services_block_for_inactive_checkin(create_person):
    """
    Testa se a Melhoria 4 está funcionando: bloqueia o lançamento de
    serviços da casa para pessoas que não possuem check-in ativo.
    """
    person = create_person

    # 1. tenta criar um serviço da casa (ex: café da manhã) para a pessoa sem check-in ativo
    with pytest.raises(ValidationError) as excinfo:
        home_service = HomeServices(person=person, breakfast=True)
        home_service.full_clean()

    # 2. verifica se a mensagem de erro da melhoria 4 foi disparada corretamente
    assert "A pessoa deve ter um check-in ativo para receber serviços." in str(
        excinfo.value.message_dict["person"]
    )
