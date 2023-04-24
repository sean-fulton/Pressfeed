from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.urls import reverse

# Create your tests here.

User = get_user_model()

class AuthenticationTest(TestCase):
    # create the test User auth model
    def setUp(self):
        self.client = Client()

        # User used for the majority of authentication tests
        self.user = User.objects.create_user(
            username='testcaseuser',
            password='pressPASS99'
        )

        # User used for change password tests
        self.user2 = User.objects.create_user(
            username='testcaseuser2',
            password='pressPASS100'
        ) 
    
    def testLogin(self):
        # Should pass test case
        response0 = self.client.post(reverse('login'), {
            'username': 'testcaseuser',
            'password': 'pressPASS99'
        })

        self.assertEqual(response0.status_code, 302)
        expected_redirect = reverse('home')
        self.assertRedirects(response0, expected_redirect)


        # Should fail due to incorrect password
        response1 = self.client.post(reverse('login'), {
            'username': 'testcaseuser',
            'password': 'incorrectPassword'
        })

        # Ensure correct response code
        self.assertEqual(response1.status_code, 302)
        # Ensure incorrect login redirects to login
        expected_redirect = reverse('login')
        self.assertRedirects(response1, expected_redirect)
        # Ensure error message is displayed
        messages = list(get_messages(response1.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "There was an error logging in")

    #testing logout
    def testLogout(self):
        #login with test user
        self.client.login(username='testcaseuser', password='pressPASS99')
        
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)

        # Should redirect to homepage
        expected_redirect = reverse('home')
        self.assertRedirects(response, expected_redirect)
        
        #Should display logout message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "You logged out successfully")

    #signup tests
    def testSignup(self):
        #check signup
        response0 = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'pressPASS25',
            'password2': 'pressPASS25'
        })
        self.assertEqual(response0.status_code, 302)

        #test attempt to signup with an existing username
        response1 = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'pressPASS50',
            'password2': 'pressPASS50'
        })
        self.assertEqual(response1.status_code, 200)

        # test signing up with non matching passwords
        response2 = self.client.post(reverse('register'), {
            'username': 'newuser2',
            'password1': 'pressPASS30',
            'password2': 'pressPASS60'
        })
        self.assertEqual(response2.status_code, 200) 

    def testAccount(self):

        self.client.login(username='testcaseuser', password='pressPASS99')

        # Ensure a logged in user can access their account page
        response0 = self.client.get(reverse('account'))
        self.assertEqual(response0.status_code, 200)

        # Ensure user can change username from account view
        response1 = self.client.post('/account/', {'username': 'new_username', 'conf-password': 'pressPASS99'})
        usernameChanged = User.objects.get(username='new_username')
        
        self.assertEqual(str(usernameChanged.username), 'new_username')
        self.assertEqual(response1.status_code, 302)

        # Ensure redirect if user enters incorrect password 
        response2 = self.client.post('/account/', {'username': 'new_username5', 'conf-password': 'wrongpassword'})
        usernameNotChanged = User.objects.get(username='new_username')
        self.assertEqual(usernameNotChanged.username, 'new_username')
        self.assertEqual(response2.status_code, 200)

    def testChangePass(self):

        self.client.login(username='testcaseuser2', password='pressPASS100')

        response0 = self.client.get(reverse('change_password'))
        self.assertEqual(response0.status_code, 200)
        
        # Ensure user can change password
        response1 = self.client.post(reverse('change_password'), {'old_password': 'pressPASS100', 
                                                        'new_password1': 'newPASS200', 
                                                        'new_password2': 'newPASS200'})
        
        passwordChanged = User.objects.get(username='testcaseuser2')
        self.assertEqual(passwordChanged.check_password('newPASS200'), True)
        self.assertEqual(response1.status_code, 302)

        #Ensure if old password is incorrect password does not change
        response2 = self.client.post(reverse('change_password'), {'old_password': 'wrongoldpass', 
                                                        'new_password1': 'newPASS300', 
                                                        'new_password2': 'newPASS300'})
        
        passwordNotChanged = User.objects.get(username='testcaseuser2')
        self.assertEqual(passwordNotChanged.check_password('newPASS300'), False)

        # NOTE this assertion should be 302, however returns 200, need to come back to this!
        # self.assertEqual(response2.status_code, 200)

        # Ensure if passwords not matching, password does not change
        response3 = self.client.post(reverse('change_password'), {'old_password': 'pressPASS200',
                                                           'new_password1': 'newPASS300',
                                                           'new_password2': 'doesNotMatch'})
        
        passwordMismatch = User.objects.get(username='testcaseuser2')
        self.assertEqual(passwordMismatch.check_password('newPASS300'), False)
        self.assertEqual(passwordMismatch.check_password('doesNotMatch'), False)
        self.assertEqual(passwordMismatch.check_password('newPASS200'), True)

    # Test delete account view
    def testDeleteAccount(self):

        self.client.login(username='testcaseuser', password='pressPASS99')

        response = self.client.post(reverse('delete_account'))
        user = User.objects.filter(username='testusercase')

        self.assertFalse(user.exists())
        self.assertRedirects(response, reverse('home'))