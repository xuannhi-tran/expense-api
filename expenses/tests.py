from django.test import TestCase
from django.contrib.auth.models import User
from expenses.models import Expense
from rest_framework.test import APIClient, force_authenticate

# Create your tests here.
class ExpenseModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="Test User", password="testuser123")
        self.expense = Expense.objects.create(name="Pizza", amount=10.00, category="Food", user=self.user)
  
    def test_expense_belongs_to_user(self):
        self.assertEqual(self.expense.user, self.user)

class ExpenseAPITest(TestCase):  
    def setUp(self):
       self.user = User.objects.create_user(username="Test User", password="testuser123")
       self.expense = Expense.objects.create(name="Pizza", amount=10.00, category="Food", user=self.user)
       self.expense3 = Expense.objects.create(name="Bus", amount=5.00, category="Transport", user=self.user)
       self.user2 = User.objects.create_user(username="Test User 2", password="testuser123")
       self.expense2 = Expense.objects.create(name="Dinner", amount=20.00, category="Food", user=self.user2)
       
       
    def test_unauthenticated_user_cannot_get_expenses(self):
        client = APIClient()
        response = client.get("/expenses/")
        self.assertEqual(response.status_code, 401)

    def test_user_can_only_see_their_expenses(self):    
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.get("/expenses/")
        self.assertEqual(response.status_code, 200)
        results = response.data["results"]
        names = [expense["name"] for expense in results]
        self.assertIn("Pizza", names)
        self.assertNotIn("Dinner", names)

    def test_user_can_create_expense(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.post(
            "/expenses/",
            data = {
                "name": "Lunch",
                "amount": 15.00,
                "category": "Food"},
            format='json' 
        )
        self.assertEqual(response.status_code, 201)
        expense = Expense.objects.get(id = response.data["id"])
        self.assertEqual(expense.name, "Lunch")
        self.assertEqual(expense.user, self.user)

    def test_create_expense_with_negative_amount_returns_400(self):  
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.post(
            "/expenses/",
            data = {
                "name": "Invalid",
                "amount": -10,
                "category": "Food" 
            },
            format="json"
        )
        self.assertEqual(response.status_code, 400)

    def test_create_expense_with_empty_name(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.post(
            "/expenses/",
            data = {
                "name":"",
                "amount":10,
                "category":"Food"
            }, format="json"
        )
        self.assertEqual(response.status_code, 400)

    
    def test_create_expense_with_empty_category(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.post(
            "/expenses/",
            data = {
                "name":"Invalid Category",
                "amount":10,
                "category":""
            }, format="json"
        )
        self.assertEqual(response.status_code, 400)

    def test_user_can_patch_their_expense(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.patch(
            f"/expenses/{self.expense.id}/",
            data = {
                "name": "Updated Pizza"
            }, format="json"
        )
        expense = Expense.objects.get(id = self.expense.id)
        self.assertEqual(expense.name, "Updated Pizza")
        self.assertEqual(response.status_code, 200)

    def test_user_can_put_their_expense(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.put(
            f"/expenses/{self.expense.id}/",
            data = {
                "name": "Updated Pizza",
                "amount": 20,
                "category": "Food"
            }, format="json"
        )
        self.assertEqual(response.status_code, 200)
        expense = Expense.objects.get(id = self.expense.id)
        self.assertEqual(expense.name, "Updated Pizza")
        self.assertEqual(expense.amount, 20)

    def test_user_can_delete_their_expense(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.delete(
            f"/expenses/{self.expense.id}/",)
        self.assertEqual(response.status_code, 204)
        with self.assertRaises(Expense.DoesNotExist):
            Expense.objects.get(id=self.expense.id)

    def test_user_A_cannot_patch_user_B_expense(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.patch(
            f"/expenses/{self.expense2.id}/",
            data = {
                "name": "Updated Dinner"
            }, format="json"
        )
        self.assertEqual(response.status_code, 404)

    def test_user_A_cannot_get_user_B_expense(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.get(
            f"/expenses/{self.expense2.id}/", format="json"
        )
        self.assertEqual(response.status_code, 404)  

    def test_user_A_cannot_delete_user_B_expense(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.delete(
            f"/expenses/{self.expense2.id}/", format="json"
        )
        self.assertEqual(response.status_code, 404)    

    def test_pagination(self):
        self.expense2 = Expense.objects.create(name="Expense2", amount=20.00, category="Food", user=self.user)
        self.expense14 = Expense.objects.create(name="Expense14", amount=10.00, category="Food", user=self.user)
        self.expense4 = Expense.objects.create(name="Expense4", amount=20.00, category="Food", user=self.user)
        self.expense5 = Expense.objects.create(name="Expense5", amount=20.00, category="Food", user=self.user)
        self.expense6 = Expense.objects.create(name="Expense6", amount=20.00, category="Food", user=self.user)
        self.expense7 = Expense.objects.create(name="Expense7", amount=20.00, category="Food", user=self.user)
        self.expense8 = Expense.objects.create(name="Expense8", amount=20.00, category="Food", user=self.user)
        self.expense9 = Expense.objects.create(name="Expense9", amount=20.00, category="Food", user=self.user)
        self.expense10 = Expense.objects.create(name="Expense10", amount=20.00, category="Food", user=self.user)
        self.expense11 = Expense.objects.create(name="Expense11", amount=20.00, category="Food", user=self.user)
        self.expense12 = Expense.objects.create(name="Expense12", amount=20.00, category="Food", user=self.user)
        self.expense13 = Expense.objects.create(name="Expense13", amount=20.00, category="Food", user=self.user)

        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.get(
            "/expenses/",
            format="json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 14)
        self.assertEqual(len(response.data["results"]), 10)
        self.assertIsNotNone(response.data["next"])

        response2 = client.get(
            "/expenses/?page=2",
            format='json'
        )
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(len(response2.data["results"]), 4)
        self.assertIsNotNone(response2.data["previous"])

    def test_filter_by_category(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.get("/expenses/?category=Transport",
                              format='json')
        self.assertEqual(response.status_code, 200)
        results = response.data["results"]
        categories = [expense["category"] for expense in results]
        self.assertNotIn("Food", categories)

    def test_search_expense(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.get("/expenses/?search=Pizza", format='json')
        self.assertEqual(response.status_code, 200)
        results = response.data["results"]
        names = [expense["name"] for expense in results]
        self.assertIn("Pizza", names)

    def test_ascending_ordering(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.get("/expenses/?ordering=amount")
        self.assertEqual(response.status_code, 200)
        expected_order = ["5.00", "10.00"]  #Pizza = 10, Bus = 5
        results = response.data["results"]
        amount = [expense["amount"] for expense in results]
        self.assertEqual(amount, expected_order)


    def test_decending_order(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.get("/expenses/?ordering=-amount")
        self.assertEqual(response.status_code, 200)
        expected_order = ["10.00", "5.00"]  #Pizza = 10, Bus = 5
        results = response.data["results"]
        amount = [expense["amount"] for expense in results]
        self.assertEqual(amount, expected_order)
        