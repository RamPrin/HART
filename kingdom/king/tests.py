from django.test import TestCase, Client
from .models import King, Kingdom, Servant

# Create your tests here.
class KingInfoTest(TestCase):
    def setUp(self) -> None:
        kingdom = Kingdom.objects.create(name='Camelot')
        King.objects.create(name='Arthur', kingdom=kingdom)

    def test_king_kingdoms(self):
        c = Client(enforce_csrf_checks=False)
        data = c.get('/api/king/1/').json()
        data1 = {
                'name': 'Arthur',
                'kingdom': {
                    'name': 'Camelot',
                    'id': 1
                },
                'accepted_servants': [],
                'not_accepted_servants': []
            }
        self.assertEqual(
            data,
            data1
        )

class TestApplyServant(TestCase):
    def setUp(self):
        kingdom = Kingdom.objects.create(name='Camelot')
        King.objects.create(name='Arthur', kingdom=kingdom)
        Servant.objects.create(name='Lancelot', kingdom=kingdom, age=17, mail='alala@ala.ala', accepted=False)
        Servant.objects.create(name='Merlin', kingdom=kingdom, age=17, mail='bdb@ala.ala', accepted=False)
        Servant.objects.create(name='Kate', kingdom=kingdom, age=17, mail='cvc@ala.ala', accepted=False)
        Servant.objects.create(name='Iwan', kingdom=kingdom, age=17, mail='dfd@ala.ala', accepted=False)
    
    def test_accept(self):
        c = Client(enforce_csrf_checks=False)
        for i in range(1, 4):
            response = c.post('/api/king/accept/', data=f'{{"id": {i}, "kingdom": 1}}'.encode(), content_type='application/json')
            self.assertEqual(response.status_code, 200)
        response = c.post('/api/king/accept/', data='{"id": 4, "kingdom": 1}'.encode(), content_type='application/json')
        self.assertEqual(response.status_code, 403)
    