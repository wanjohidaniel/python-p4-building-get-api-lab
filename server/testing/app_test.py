import json
from app import app, db, Bakery, BakedGood

class TestApp:
    '''Flask application in flask_app.py'''

    def setup_method(self):
        """Set up the test database."""
        with app.app_context():
            db.create_all()

    def teardown_method(self):
        """Tear down the test database."""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_bakeries_route(self):
        '''has a resource available at "/bakeries".'''
        response = app.test_client().get('/bakeries')
        assert response.status_code == 200

    def test_bakeries_route_returns_json(self):
        '''provides a response content type of application/json at "/bakeries"'''
        response = app.test_client().get('/bakeries')
        assert response.content_type == 'application/json'

    def test_bakeries_route_returns_list_of_bakery_objects(self):
        '''returns JSON representing models.Bakery objects.'''
        with app.app_context():
            b = Bakery(name="My Bakery")
            db.session.add(b)
            db.session.commit()

            response = app.test_client().get('/bakeries')
            data = json.loads(response.data.decode())
            assert type(data) == list
            
            contains_my_bakery = False
            for record in data:
                assert type(record) == dict
                assert 'id' in record
                assert 'name' in record
                assert 'created_at' in record
                if record['name'] == "My Bakery":
                    contains_my_bakery = True
            assert contains_my_bakery

    def test_bakery_by_id_route(self):
        '''has a resource available at "/bakeries/<int:id>".'''
        with app.app_context():
            b = Bakery(name="My Bakery")
            db.session.add(b)
            db.session.commit()

            response = app.test_client().get(f'/bakeries/{b.id}')
            assert response.status_code == 200

    def test_bakery_by_id_route_returns_json(self):
        '''provides a response content type of application/json at "/bakeries/<int:id>"'''
        with app.app_context():
            b = Bakery(name="My Bakery")
            db.session.add(b)
            db.session.commit()

            response = app.test_client().get(f'/bakeries/{b.id}')
            assert response.content_type == 'application/json'

    def test_bakery_by_id_route_returns_one_bakery_object(self):
        '''returns JSON representing one models.Bakery object.'''
        with app.app_context():
            b = Bakery(name="My Bakery")
            db.session.add(b)
            db.session.commit()

            response = app.test_client().get(f'/bakeries/{b.id}')
            data = json.loads(response.data.decode())
            assert type(data) == dict
            assert data['id'] == b.id
            assert data['name'] == "My Bakery"
            assert 'created_at' in data

    def test_baked_goods_by_price_route(self):
        '''has a resource available at "/baked_goods/by_price".'''
        response = app.test_client().get('/baked_goods/by_price')
        assert response.status_code == 200
    
    def test_baked_goods_by_price_route_returns_json(self):
        '''provides a response content type of application/json at "/baked_goods/by_price"'''
        response = app.test_client().get('/baked_goods/by_price')
        assert response.content_type == 'application/json'

    def test_baked_goods_by_price_returns_list_of_baked_goods_in_descending_order(self):
        '''returns JSON representing one models.Bakery object.'''
        with app.app_context():
            b1 = BakedGood(name="Madeleine", price=50)
            b2 = BakedGood(name="Donut", price=25)
            db.session.add_all([b1, b2])
            db.session.commit()

            response = app.test_client().get('/baked_goods/by_price')
            data = json.loads(response.data.decode())
            assert type(data) == list
            for record in data:
                assert 'id' in record
                assert 'name' in record
                assert 'price' in record
                assert 'created_at' in record
            
            prices = [record['price'] for record in data]
            assert all(prices[i] >= prices[i+1] for i in range(len(prices) - 1))

    def test_most_expensive_baked_good_route_returns_json(self):
        '''provides a response content type of application/json at "/bakeries/<int:id>"'''
        response = app.test_client().get('/baked_goods/most_expensive')
        assert response.content_type == 'application/json'

    def test_most_expensive_baked_good_route_returns_one_baked_good_object(self):
        '''returns JSON representing one models.BakedGood object.'''
        with app.app_context():
            b1 = BakedGood(name="Madeleine", price=50)
            b2 = BakedGood(name="Donut", price=25)
            db.session.add_all([b1, b2])
            db.session.commit()

            response = app.test_client().get('/baked_goods/most_expensive')
            data = json.loads(response.data.decode())
            assert type(data) == dict
            assert 'id' in data
            assert 'name' in data
            assert 'price' in data
            assert 'created_at' in data

    def test_most_expensive_baked_good_route_returns_most_expensive_baked_good_object(self):
        '''returns JSON representing one models.BakedGood object.'''
        with app.app_context():
            b1 = BakedGood(name="Madeleine", price=50)
            b2 = BakedGood(name="Donut", price=25)
            db.session.add_all([b1, b2])
            db.session.commit()

            response = app.test_client().get('/baked_goods/most_expensive')
            data = json.loads(response.data.decode())
            assert data['price'] == b1.price
