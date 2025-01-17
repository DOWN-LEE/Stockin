'''
tests_groups
'''
import os
import json

from django.test import TestCase, Client
from core.models import Group, Stock


pwd = os.getenv("BACK_TEST_PWD").split(',')[0]

class GroupsTestCase(TestCase):
    '''
    GroupsTestCase
    '''
    def test_group_create(self):
        '''
        test_group_create
        '''
        client = Client(enforce_csrf_checks=True)

        # test 1
        response = client.get('/api/users/token/')
        csrftoken = response.cookies['csrftoken'].value

        response = client.get('/api/groups/', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code, 401)

        response = client.post('/api/groups/', json.dumps({'name': 'test'}),
                    content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code, 401)

        # test 2
        response = client.get('/api/users/token/')
        csrftoken = response.cookies['csrftoken'].value
        response = client.post('/api/users/signup/',
                    json.dumps({'email': 'normal@user.com', 'nickname': 'user', 'password': pwd}),
                    content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)

        response = client.get('/api/users/token/')
        csrftoken = response.cookies['csrftoken'].value
        response = client.post('/api/users/signin/',
                    json.dumps({'email': 'normal@user.com', 'nickname': 'user', 'password': pwd}),
                    content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)

        response = client.get('/api/users/token/')
        csrftoken = response.cookies['csrftoken'].value
        response = client.post('/api/groups/', json.dumps({'foo': 'test'}),
                    content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code, 400)

        # test 3
        response = client.post('/api/groups/', json.dumps({'name': 'test'}),
                    content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        response = client.post('/api/groups/', json.dumps({'name': 'test'}),
                    content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code, 201)

        # test 4
        Stock.objects.create(title='test_stock1', code='test_code1', sector='test_sector1')

        response = client.get('/api/users/token/')
        csrftoken = response.cookies['csrftoken'].value
        response = client.post('/api/groups/1/stocks/', json.dumps({'id': '1'}),
                    content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)

        response = client.get('/api/groups/')
        self.assertEqual(response.status_code, 200)

        # HttpResponseNotAllowed tests
        response = client.get('/api/users/token/')
        csrftoken = response.cookies['csrftoken'].value
        response = client.delete('/api/groups/', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code, 405)

    def test_group_edit_e(self):
        '''
        test_group_edit_e
        '''
        client = Client(enforce_csrf_checks=True)
        response = client.get('/api/groups/')

        # test 1
        response = client.get('/api/users/token/')
        csrftoken = response.cookies['csrftoken'].value

        response = client.put('/api/groups/1/',
                    json.dumps({'name': 'test'}), HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code, 401)

        response = client.delete('/api/groups/1/', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code, 401)

        response = client.get('/api/users/token/')
        csrftoken = response.cookies['csrftoken'].value
        response = client.post('/api/users/signup/',
                    json.dumps({'email': 'normal@user.com', 'nickname': 'user', 'password': pwd}),
                    content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)

        response = client.get('/api/users/token/')
        csrftoken = response.cookies['csrftoken'].value
        response = client.post('/api/users/signin/',
                    json.dumps({'email': 'normal@user.com', 'nickname': 'user', 'password': pwd}),
                    content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code, 201)

        response = client.get('/api/users/token/')
        csrftoken = response.cookies['csrftoken'].value
        response = client.put('/api/groups/1/',
                    json.dumps({'name': 'test'}), HTTP_X_CSRFTOKEN=csrftoken)

        self.assertEqual(response.status_code, 404)

        response = client.get('/api/users/token/')
        csrftoken = response.cookies['csrftoken'].value
        response = client.post('/api/groups/', json.dumps({'name': 'test'}),
                    content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code, 201)

        target_id = json.loads(response.content)['id']

        response = client.get('/api/users/token/')
        csrftoken = response.cookies['csrftoken'].value
        response = client.put('/api/groups/'+str(target_id)+'/',
                    json.dumps({'foo': 'test'}), HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code, 400)

        response = client.get('/api/users/token/')
        csrftoken = response.cookies['csrftoken'].value
        response = client.delete('/api/groups/10/', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code, 404)


    def test_group_edit(self):
        '''
        test_group_edit
        '''
        client = Client(enforce_csrf_checks=True)
        # PUT request
        response = client.get('/api/users/token/')
        csrftoken = response.cookies['csrftoken'].value
        response = client.post('/api/users/signup/',
                    json.dumps({'email': 'normal@user.com', 'nickname': 'user', 'password': pwd}),
                    content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)

        response = client.get('/api/users/token/')
        csrftoken = response.cookies['csrftoken'].value
        response = client.post('/api/users/signin/',
                    json.dumps({'email': 'normal@user.com', 'nickname': 'user', 'password': pwd}),
                    content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code, 201)

        response = client.get('/api/users/token/')
        csrftoken = response.cookies['csrftoken'].value
        response = client.post('/api/groups/', json.dumps({'name': 'test'}),
                    content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code, 201)

        target_id = json.loads(response.content)['id']

        response = client.get('/api/users/token/')
        csrftoken = response.cookies['csrftoken'].value
        response = client.put('/api/groups/'+str(target_id)+'/',
                    json.dumps({'name': 'new_test'}), HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code, 200)

        response = client.get('/api/users/signout')

        response = client.get('/api/users/token/')
        csrftoken = response.cookies['csrftoken'].value
        response = client.post('/api/users/signup/',
                    json.dumps({'email':'normal2@user.com', 'nickname':'user2', 'password':pwd}),
                    content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)

        response = client.get('/api/users/token/')
        csrftoken = response.cookies['csrftoken'].value
        response = client.post('/api/users/signin/',
                    json.dumps({'email':'normal2@user.com', 'nickname':'user2', 'password':pwd}),
                    content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)

        response = client.get('/api/users/token/')
        csrftoken = response.cookies['csrftoken'].value
        response = client.put('/api/groups/'+str(target_id)+'/',
                    json.dumps({'name': 'new_test'}), HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code, 403)

        response = client.get('/api/users/signout/')

        # DELETE request
        response = client.get('/api/users/token/')
        csrftoken = response.cookies['csrftoken'].value
        response = client.post('/api/users/signin/',
                    json.dumps({'email': 'normal2@user.com', 'nickname': 'user', 'password': pwd}),
                    content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)

        response = client.get('/api/users/token/')
        csrftoken = response.cookies['csrftoken'].value
        response = client.delete('/api/groups/'+str(target_id)+'/', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code, 403)

        response = client.get('/api/users/signout')

        response = client.get('/api/users/token/')
        csrftoken = response.cookies['csrftoken'].value
        response = client.post('/api/users/signin/',
                    json.dumps({'email': 'normal@user.com', 'nickname': 'user', 'password': pwd}),
                    content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)

        response = client.get('/api/users/token/')
        csrftoken = response.cookies['csrftoken'].value
        response = client.delete('/api/groups/'+str(target_id)+'/', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code, 200)

        # HttpResponseNotAllowed tests
        response = client.get('/api/groups/1/')
        self.assertEqual(response.status_code, 405)


    def test_group_stock_list_e(self):
        '''
        test_group_stock_list_e
        '''
        client = Client(enforce_csrf_checks=True)

        # test 1
        response = client.get('/api/groups/1/stocks/')
        self.assertEqual(response.status_code, 401)

        response = client.get('/api/users/token/')
        csrftoken = response.cookies['csrftoken'].value
        response = client.post('/api/groups/1/stocks/', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code, 401)

        response = client.get('/api/users/token/')
        csrftoken = response.cookies['csrftoken'].value
        response = client.post('/api/users/signup/',
                    json.dumps({'email': 'normal@user.com', 'nickname': 'user', 'password': pwd}),
                    content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)

        response = client.get('/api/users/token/')
        csrftoken = response.cookies['csrftoken'].value
        response = client.post('/api/users/signin/',
                    json.dumps({'email': 'normal@user.com', 'nickname': 'user', 'password': pwd}),
                    content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)

        response = client.get('/api/groups/1/stocks/')
        self.assertEqual(response.status_code, 404)

        response = client.get('/api/users/token/')
        csrftoken = response.cookies['csrftoken'].value
        response = client.post('/api/groups/10/stocks/', json.dumps({'id': 1}),
                    content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code, 404)


    def test_group_stock_list(self):
        '''
        test_group_stock_list
        '''
        client = Client(enforce_csrf_checks=True)

        # GET request
        response = client.get('/api/users/token/')
        csrftoken = response.cookies['csrftoken'].value
        response = client.post('/api/users/signup/',
                    json.dumps({'email': 'normal@user.com', 'nickname': 'user', 'password': pwd}),
                    content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)

        response = client.get('/api/users/token/')
        csrftoken = response.cookies['csrftoken'].value
        response = client.post('/api/users/signin/',
                    json.dumps({'email': 'normal@user.com', 'nickname': 'user', 'password': pwd}),
                    content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)

        test_stock1 = Stock.objects.create(title='test_article',
                                            code='test_code',
                                            sector='test_sector')
        response = client.get('/api/users/token/')
        csrftoken = response.cookies['csrftoken'].value
        response = client.post('/api/groups/', json.dumps({'name': 'test'}),
                    content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        Group.objects.get(name='test').stocks.add(test_stock1)

        target_id = json.loads(response.content)['id']

        response = client.get('/api/groups/1/stocks/')

        response = client.get('/api/users/signout/')

        response = client.get('/api/users/token/')
        csrftoken = response.cookies['csrftoken'].value
        response = client.post('/api/users/signup/',
                    json.dumps({'email': 'normal2@user.com', 'nickname':'user2', 'password': pwd}),
                    content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)

        response = client.get('/api/users/token/')
        csrftoken = response.cookies['csrftoken'].value
        response = client.post('/api/users/signin/',
                    json.dumps({'email': 'normal2@user.com', 'nickname':'user2', 'password': pwd}),
                    content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)

        response = client.get('/api/groups/'+str(target_id)+'/stocks/')
        self.assertEqual(response.status_code, 403)

        # POST request

        response = client.get('/api/users/token/')
        csrftoken = response.cookies['csrftoken'].value
        response = client.post('/api/groups/'+str(target_id)+'/stocks/', json.dumps({'id': 1}),
                    content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code, 403)

        response = client.get('/api/users/signout/')

        response = client.get('/api/users/token/')
        csrftoken = response.cookies['csrftoken'].value
        response = client.post('/api/users/signin/',
                    json.dumps({'email': 'normal@user.com', 'nickname': 'user', 'password': pwd}),
                    content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)

        # TO-DO : stock 모델 추가 후 group 에 stock 추가
        test_stock2 = Stock.objects.create(title='test_article2',
                                            code='test_code2',
                                            sector='test_sector2')

        response = client.get('/api/users/token/')
        csrftoken = response.cookies['csrftoken'].value
        response = client.post('/api/groups/'+str(target_id)+'/stocks/',
                    json.dumps({'id': test_stock1.id}),
                    content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code, 204)

        response = client.get('/api/users/token/')
        csrftoken = response.cookies['csrftoken'].value
        response = client.post('/api/groups/'+str(target_id)+'/stocks/',
                    json.dumps({'id': test_stock2.id}),
                    content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code, 201)

        response = client.get('/api/users/token/')
        csrftoken = response.cookies['csrftoken'].value
        response = client.post('/api/groups/'+str(target_id)+'/stocks/',
                    json.dumps({'id': test_stock2.id+1}),
                    content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code, 404)

        # response = client.get('/api/users/token/')
        # csrftoken = response.cookies['csrftoken'].value
        # response = client.post('/api/groups/'+str(target_id)+'/stocks/',
        #             json.dumps({'invalid': 1}),
        #             content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        # self.assertEqual(response.status_code, 400)

        # HttpResponseNotAllowed tests
        response = client.get('/api/users/token/')
        csrftoken = response.cookies['csrftoken'].value
        response = client.delete('/api/groups/1/stocks/', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code, 405)


    def test_group_stock_delete(self):
        '''
        test_group_stock_delete
        '''
        client = Client(enforce_csrf_checks=True)
        test_stock = Stock.objects.create(title='test_article',
                                            code='test_code',
                                            sector='test_sector')

        # test 1
        response = client.get('/api/users/token/')
        csrftoken = response.cookies['csrftoken'].value
        response = client.delete('/api/groups/1/stocks/1/', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code, 401)

        # DELETE request
        response = client.get('/api/users/token/')
        csrftoken = response.cookies['csrftoken'].value
        response = client.post('/api/users/signup/',
                    json.dumps({'email': 'normal@user.com', 'nickname': 'user', 'password': pwd}),
                    content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)

        response = client.get('/api/users/token/')
        csrftoken = response.cookies['csrftoken'].value
        response = client.post('/api/users/signin/',
                    json.dumps({'email': 'normal@user.com', 'nickname': 'user', 'password': pwd}),
                    content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)

        response = client.get('/api/users/token/')
        csrftoken = response.cookies['csrftoken'].value
        response = client.delete('/api/groups/1/stocks/1/', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code, 404)

        response = client.get('/api/users/token/')
        csrftoken = response.cookies['csrftoken'].value
        response = client.post('/api/groups/', json.dumps({'name': 'test'}),
                    content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)

        target_id = json.loads(response.content)['id']

        response = client.get('/api/users/token/')
        csrftoken = response.cookies['csrftoken'].value
        response = client.delete('/api/groups/'+str(target_id)+'/stocks/'+str(test_stock.id+1)+'/',
                    HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code, 404)

        response = client.get('/api/users/token/')
        csrftoken = response.cookies['csrftoken'].value
        response = client.post('/api/groups/'+str(target_id)+'/stocks/',
                    json.dumps({'id': test_stock.id}),
                    content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code, 201)

        response = client.get('/api/users/token/')
        csrftoken = response.cookies['csrftoken'].value
        response = client.delete('/api/groups/'+str(target_id)+'/stocks/'+str(test_stock.id)+'/',
                    HTTP_X_CSRFTOKEN=csrftoken)
        #self.assertEqual(response.status_code, 200)

        test_stock2 = Stock.objects.create(title='test_article2',
                                            code='test_code2',
                                            sector='test_sector2')

        # Remove has no error although have no target delete models
        response = client.get('/api/users/token/')
        csrftoken = response.cookies['csrftoken'].value
        response = client.delete('/api/groups/'+str(target_id)+'/stocks/'+str(test_stock2.id)+'/',
                    HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code, 200)

        response = client.get('/api/users/signout/')

        response = client.get('/api/users/token/')
        csrftoken = response.cookies['csrftoken'].value
        response = client.post('/api/users/signup/',
                    json.dumps({'email': 'normal2@user.com', 'nickname':'user2', 'password':pwd}),
                    content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)

        response = client.get('/api/users/token/')
        csrftoken = response.cookies['csrftoken'].value
        response = client.post('/api/users/signin/',
                    json.dumps({'email': 'normal2@user.com', 'nickname':'user2', 'password':pwd}),
                    content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)

        response = client.get('/api/users/token/')
        csrftoken = response.cookies['csrftoken'].value
        response = client.delete('/api/groups/'+str(target_id)+'/stocks/'+str(test_stock.id)+'/',
                    HTTP_X_CSRFTOKEN=csrftoken)
        self.assertEqual(response.status_code, 403)

        # HttpResponseNotAllowed tests
        response = client.get('/api/groups/1/stocks/1/')
        self.assertEqual(response.status_code, 405)

    def test_get_group_list(self):
        '''
        test_get_group_list
        '''
        client = Client(enforce_csrf_checks=True)
        response = client.get('/api/users/token/')
        csrftoken = response.cookies['csrftoken'].value
        response = client.post('/api/users/signup/',
                    json.dumps({'email': 'normal@user.com', 'nickname': 'user', 'password': pwd}),
                    content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)

        response = client.get('/api/users/token/')
        csrftoken = response.cookies['csrftoken'].value
        response = client.post('/api/users/signin/',
                    json.dumps({'email': 'normal@user.com', 'nickname': 'user', 'password': pwd}),
                    content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)

        response = client.get('/api/users/token/')
        csrftoken = response.cookies['csrftoken'].value
        response = client.post('/api/groups/', json.dumps({'name': 'test'}),
                    content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)

        target_id = json.loads(response.content)['id']
        test_stock = Stock.objects.create(title='test')

        response = client.get('/api/users/token/')
        csrftoken = response.cookies['csrftoken'].value
        response = client.post('/api/groups/'+str(target_id)+'/stocks/',
                    json.dumps({'id': test_stock.id}),
                    content_type='application/json', HTTP_X_CSRFTOKEN=csrftoken)

        response = client.get('/api/groups/')
        self.assertEqual(response.status_code, 200)
