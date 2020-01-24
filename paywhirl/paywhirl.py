"""PayWhirl API Client
====================

This library has been made available to simplify
interfacing with PayWhirl's API
located at [api.paywhirl.com](https://api.paywhirl.com)

API keys can be obtained after making an account on
[PayWhirl's account page](https://app.paywhirl.com/api-keys)

Example Usage:
--------------
```
from paywhirl import PayWhirl, HTTPError

api_key = 'pwpk_xxxxxxxxxxxxxxx'
api_secret = 'pwpsk_xxxxxxxxxxx'

pw = PayWhirl(api_key, api_secret)

try:
    print(pw.get_account())
except HTTPError as e:
    print(e.response.status_code)
    print(e.response.text)
```

For information on type hints in Python 3.5 and higher see
https://www.python.org/dev/peps/pep-0484/
"""

from typing import Any
import requests

HTTPError = requests.exceptions.HTTPError

class PayWhirl: # pylint: disable=too-many-public-methods
    """PayWhirl API client"""

    _api_key: str
    _api_secret: str
    _api_base: str
    _verify_ssl: bool

    def __init__(
            self,
            api_key: str,
            api_secret: str,
            api_base: str = 'https://api.paywhirl.com') -> None:
        """Initialize the paywhirl object for making requests.

        Args:
            api_key: the api key for your account
            api_secret: your secret key
            api_base: the target URL for requests.
                Defaults to 'https://api.paywhirl.com'
        """

        self._api_key = api_key
        self._api_secret = api_secret
        self._api_base = api_base
        self._verify_ssl = True

    def get_customers(self, data: dict) -> list:
        """Get a list of customers associated with your account.

        Args:
            data:
                {
                    'limit': (int),
                    'order_key': (str),
                    'order_direction': (str),
                    'before_id': (int),
                    'after_id': (int),
                    'keyword': (str)
                }

                'limit' defaults to 100. 'order_key' defaults to 'id'.
                'order_direction' options are 'asc' and 'desc'
                for ascend and descend, respectively.
                'before_id' returns all customers less than the
                specified id, and 'after_id' returns
                all customers greater than the specified id.
                'keyword' will filter the results by the chosen string.

        Returns:
            A list of customer dicts filtered by your arguments,
            or an error message indicating what went wrong.
        """

        return self._get('/customers', data)

    def get_customer(self, customer_id: int) -> Any:
        """Get a single customer.

        Args:
            customer_id: the id number obtained from paywhirl's servers.
                (use the get_customers() method to find your IDs)

        Returns:
            A dictionary with complete customer data
            or an error message indicating what went wrong.
        """

        return self._get(str.format('/customer/{0}', customer_id))

    def get_addresses(self, customer_id: int) -> Any:
        """Get all addresses associated with a single customer

        Args:
            customer_id: the id number obtained from paywhirl's servers.
                (use the get_customers() method to find your IDs)

        Returns:
            A dictionary with a list of addresses associated with the
            customer
            or an error message indicating what went wrong.
        """

        return self._get(str.format('/customer/addresses/{0}', customer_id))

    def get_address(self, address_id: int) -> Any:
        """Get all addresses associated with a single customer

        Args:
            address_id: the id number obtained from paywhirl's servers.
                (use the get_addresses() method to find your IDs)

        Returns:
            An address associated with the given id
            or an error message indicating what went wrong.
        """

        return self._get(str.format('/customer/address/{0}', address_id))

    def get_profile(self, customer_id: int) -> Any:
        """Get a full profile for a given customer. This includes
            the customer, the addresses, and the answers to profile
            questions.

        Args:
            customer_id: the id number obtained from paywhirl's servers.
                (use the get_addresses() method to find your IDs)

        Returns:
            A dictionary associated with the given id that includes
            customer, addresses, and profile answers
            or an error message indicating what went wrong.
        """

        return self._get(str.format('/customer/profile/{0}', customer_id))

    def auth_customer(self, email: str, password: str) -> Any:
        """Authenticate a customer with supplied data.

        Args:
            email: customer's email address
            password: plain-text or bcrypt hashed password

        Returns:
            Dictionary with status 'success' or 'failure'.
        """

        data = {'email': email, 'password': password}
        return self._post('/auth/customer', data)

    def create_customer(self, data: dict) -> Any:
        """Create a new customer with supplied data.

        Args:
            data:
                {
                    'first_name': (str),
                    'last_name': (str),
                    'email': (str),
                    'password': (str),
                    'currency': (str)
                }

            Only the required key: value pairs are listed above,
            more information about additional options can be found
            on the docs site located in the header of this file.

        Returns:
            A response containing either the created customer dictionary
            or an error message indicating what went wrong.
        """

        return self._post('/create/customer', data)

    def update_customer(self, data: dict) -> Any:
        """Update an existing customer (selected by id) with new info.

        Args:
            data:
                {
                    'id': (int),
                    ...
                }

            Any element existing in a current customer object should
            be a viable key-value pair to pass in for modification.

        Returns:
            A dict containing either the updated customer
            or an error message indicating what went wrong.
        """

        return self._post('/update/customer', data)

    def delete_customer(self, customer_id: int, forget: int = None) -> Any:
        """Delete an existing customer by its ID.

        Args:
            customer_id: this can be found via the get_customers() method.
            forget: send 1 to make this customer data obfuscated besides soft-deleted.

        Returns:
            A dictionary with {'status: 'success' or 'fail'}
            or an error message indicating what went wrong.
        """

        data = dict([('id', customer_id)])
        if forget is not None:
            data['forget'] = forget
        return self._post('/delete/customer', data)

    def get_questions(self, return_list_size: int = 100) -> Any:
        """Retrieve a list of all questions associated with your
           account.

        Args:
            return_list_size: on a successful query, this will
                specify the number of elements in the returned list.
                Default value is 100.

        Returns:
            A list containing answer dicts,
            or an error message indicating what went wrong.
        """

        data = {'limit': return_list_size}
        return self._get('/questions', data)

    def update_answer(self, data: dict) -> Any:
        """Update an existing answer with new info.

        Args:
            data:
                {
                    'customer_id': (int),
                    'question_name': (str),
                    'answer': (str),
                    'address_id': (int)
                }

        Returns:
            A dict containing either the updated answer,
            a list of answers,
            or an error message indicating what went wrong.
        """

        return self._post('/update/answer', data)

    def get_answers(self, customer_id: int) -> Any:
        """Get a list of answers associated with a customer.

        Args:
            customer_id: the 'id' value from a customer dict.
                you can find this via the get_customers() method.

        Returns:
            A list containing answer dictionaries,
            or an error message indicating what went wrong.
        """

        data = {'customer_id': customer_id}
        return self._get('/answers', data)

    def get_plans(self, data: dict) -> Any:
        """Get a list of plans associated with your account.

        Args:
            data:
            {
                'limit': (int),
                'order_key': (str),
                'order_direction': (str),
                'before_id': (int),
                'after_id': (int)
            }

            'limit' defaults to 100. 'order_key' defaults to 'id'.
            'order_direction' can be 'asc' or 'desc'. Defaults to
            descending. 'before_id' and 'after_id' will return plans
            with 'id's less than or greater than the selected 'id'
            number, respectively.

        Returns:
            A list containing plan dictionaries,
            or an error message indicating what went wrong.
        """

        return self._get('/plans', data)

    def get_plan(self, plan_id: int) -> Any:
        """Get a single plan using the plan's ID

        Args:
            plan_id: the id number obtained from paywhirl's servers.
                (use the get_plans() method to find your IDs)
        Returns:
            A dictionary with data for a given plan
            or an error message indicating what went wrong.
        """

        return self._get(str.format('/plan/{0}', plan_id))

    def create_plan(self, data: dict) -> Any:
        """Create a plan to set rules for how a customer will be billed.

        Args:
            data: A dictionary containing plan rules.
            See the docs linked in the header for more info.

        Returns:
            A dictionary containing the created plan
            or an error message indicating what went wrong.
        """

        return self._post('/create/plan', data)

    def update_plan(self, data: dict) -> Any:
        """Update an existing plan selected by a plan's 'id' member.

        Args:
            data: A dictionary containing plan rules. the 'id' field
                is required.
            See the docs linked in the header for more info.

        Returns:
            A dictionary containing the updated plan
            or an error message indicating what went wrong.
        """

        return self._post('/update/plan', data)

    def get_subscriptions(self, customer_id: int) -> Any:
        """Retrieve a list of all subscriptions for a given customer.

        Args:
            customer_id: This can be found using the get_customers()
                method.

        Returns:
            A list containing plan dictionaries
            or an error message indicating what went wrong.
        """

        return self._get(str.format('/subscriptions/{0}', customer_id))

    def get_subscription(self, subscription_id: int) -> Any:
        """Retrieve a single subscription by passing in an ID.

        Args:
            subscription_id: These can be found by using the
                get_subscriptions() method.

        Returns:
            A single dict containing subscription information
            or an error message indicating what went wrong.
        """

        return self._get(str.format('/subscription/{0}', subscription_id))

    def subscribe_customer(self, data: dict) -> Any:
        """Subscribe a customer to a given plan.

        Args:
            data:
                {
                    'customer_id': (int),
                    'plan_id': (int),
                    'quantity': (int),
                    'promo_id': (int),
                    'trial_end': (int)
                }
            customer_id: The existing customer. (These can be found
                with the get_customers() method).

            plan_id: The plan to subscribe to. (These can be found
                with the get_plans() method).

            trial_end(optional): A UNIX timestamp indicating when a
                trial period should end. The docs linked in the header
                have extra information on how to generate these.
                Defaults to no trial.

            promo_id(optional): An existing promo code ID number.
                (These can be found with the get_promos() method).

            quantity(optional): Number of subscriptions to subscribe to.
                This defaults to 1.

        Returns:
            A dictionary containing information about the subscription
            or an error message indicating what went wrong.
        """

        return self._post('/subscribe/customer', data)

    def update_subscription(self, # pylint: disable=too-many-arguments
                            subscription_id: int,
                            plan_id: int,
                            quantity: int = None,
                            address_id: int = None,
                            installments_left: int = None,
                            trial_end: int = None,
                            card_id: int = None) -> Any:
        """Change a customer's subscription to a different plan.

        Args:
            subscription_id: The current subscription id.
            plan_id: The new plan for the subscription.

        Returns:
            A dictionary containing information about the subscription
            or an error message indicating what went wrong.
        """

        data = {
            'subscription_id': subscription_id,
            'plan_id': plan_id
        }

        if quantity is not None:
            data['quantity'] = quantity
        if address_id is not None:
            data['address_id'] = address_id
        if installments_left is not None:
            data['installments_left'] = installments_left
        if trial_end is not None:
            data['trial_end'] = trial_end
        if card_id is not None:
            data['card_id'] = card_id

        return self._post('/update/subscription', data)

    def unsubscribe_customer(self, subscription_id: int) -> Any:
        """Cancel a customer's existing subscription.

        Args:
            subscription_id: You can find these by using the
                get_subscriptions() method for a given customer.

        Returns:
            A dictionary with {'status: 'success' or 'fail'}
            or an error message indicating what went wrong.
        """

        data = dict([('subscription_id', subscription_id)])
        return self._post('/unsubscribe/customer', data)

    def get_subscribers(self, data: dict) -> Any:
        """Get a list of all active subscribers.

        Args:
            data:
            {
                'limit': (int),
                'order': (str),
                'keyword': (str),
                'starting_after': (int),
                'starting_before': (int)
            }

            'limit' defaults to 20.
            'order' can be 'asc', 'desc', or 'rand'.
            'starting_after' will return subscribers with
            subscription IDs greater than 'starting_after'.
            'starting_before' will return subscribers with
            subscription IDs greater than 'starting_before'.
            'keyword' will filter the results by that word.

        Returns:
            A list containing subscriber dictionaries,
            or an error message indicating what went wrong.
        """

        return self._get('/subscribers', data)

    def get_invoice(self, invoice_id: int) -> Any:
        """Get the data for a single invoice when given an ID number.

        Args:
            invoice_id: Pass in a known invoice ID or use get_invoices()
                to get a collection of them from a single customer.

        Returns:
            A dictionary containing information about the selected
            invoice, or an error message indicating what went wrong.
        """

        return self._get(str.format('/invoice/{0}', invoice_id))

    def get_invoices(self, customer_id: int, all_invoices: bool = False) -> Any:
        """Get a list of upcoming invoices for a specified customer.

        Args:
            customer_id: These can be found using the get_customers()
                method.

        Returns:
            A dictionary or list of dictionaries containing invoice
            data, or an error message indicating what went wrong.
        """

        params = {'all': '1' if all_invoices else ''}
        return self._get(str.format('/invoices/{0}', customer_id), params)

    def process_invoice(self, invoice_id: int, data: dict) -> Any:
        """Process an upcoming invoice by invoice id

        Args:
            invoice_id: Pass in a known invoice ID or use get_invoices()
                to get a collection of them from a single customer.
            data: a dictionary with additional processing params
            See api.paywhirl.com documentation for details
        Returns:
            Success or Fail
        """
        return self._post(str.format('/invoice/{0}/process', invoice_id), data)

    def mark_invoice_as_paid(self, invoice_id: int) -> Any:
        """Mark an upcoming invoice as paid by invoice id

        Args:
            invoice_id: Pass in a known invoice ID or use get_invoices()
                to get a collection of them from a single customer.
        Returns:
            Success or Fail
        """
        return self._post(str.format('/invoice/{0}/mark-as-paid', invoice_id))

    def add_promo_code_to_invoice(self, invoice_id: int, promo_code: str) -> Any:
        """Add a promo code to an upcoming invoice

        Args:
            invoice_id: Pass in a known invoice ID or use get_invoices()
                to get a collection of them from a single customer.
            promo_code: The promo code to apply.
        Returns:
            Success or Fail
        """
        data = dict([('promo_code', promo_code)])
        return self._post(str.format('/invoice/{0}/add-promo', invoice_id), data)

    def remove_promo_code_from_invoice(self, invoice_id: int) -> Any:
        """Remove promo code from an upcoming invoice

        Args:
            invoice_id: Pass in a known invoice ID or use get_invoices()
                to get a collection of them from a single customer.
        Returns:
            Success or Fail
        """
        return self._post(str.format('/invoice/{0}/remove-promo', invoice_id))

    def update_invoice_card(self, invoice_id: int, card_id: int) -> Any:
        """Change the card associated with a given invoice

        Args:
            invoice_id: Pass in a known invoice ID or use get_invoices()
                to get a collection of them from a single customer.
            card_id: Pass in a known card ID to set active card.
        Returns:
            Success or Fail
        """
        data = {'card_id': card_id}
        return self._post(str.format('/invoice/{0}/card', invoice_id), data)

    def update_invoice_items(self, invoice_id: int, line_items: dict) -> Any:
        """Change the number of line items in a give invoice

        Args:
            invoice_id: Pass in a known invoice ID or use get_invoices()
                to get a collection of them from a single customer.
            line_items: Pass in a dictionary of item ids and the updated quantity
                example:{'1111': 4, '1112', 5}
        Returns:
            Success or Fail, and number of items changed
        """
        return self._post(str.format('/invoice/{0}/items', invoice_id), line_items)


    def create_invoice(self, data: dict) -> Any:
        """Create a new invoice

        Args:
            data: a dictionary describing the invoice and the items
            See api.paywhirl.com documentation for details
        Returns:
            Success or Fail and invoice_id
        """
        return self._post('/invoices', data)

    def delete_invoice(self, invoice_id: int) -> Any:
        """Delete an existing invoice by its ID number.

        Args:
            invoice_id: this can be found via the get_invoices() method.

        Returns:
            A dictionary with {'status: 'success' or 'fail'}
            or an error message indicating what went wrong.
        """

        data = dict([('id', invoice_id)])
        return self._post('/delete/invoice', data)

    def get_gateways(self) -> Any:
        """Returns a list of your payment gateways.

        Returns:
            A dictionary or list of dictionaries containing gateway
            data, or an error message indicating what went wrong.
        """

        return self._get('/gateways')

    def get_gateway(self, gateway_id: int) -> Any:
        """Get a gateway specified by its ID number.

        Args:
            gateway_id: this can be found using get_gateways().

        Returns:
            A dictionary or list of dictionaries containing gateway
            data, or an error message indicating what went wrong.
        """

        return self._get(str.format('/gateway/{0}', gateway_id))

    def create_charge(self, data: dict) -> Any:
        """Attempt to a customer and return an invoice.

        Args:
            dict:
                See docs linked in the header for param options.

        Returns:
            A dictionary containing an invoice, or an error message
            indicating what went wrong.
        """

        return self._post('/create/charge', data)

    def get_charge(self, charge_id: int) -> Any:
        """Get a single charge using the charge ID.

        Args:
            charge_id: these can be found in each invoice.

        Returns:
            A dictionary containing charge information, or an error
            message indicating what went wrong.
        """

        return self._get(str.format('/charge/{0}', charge_id))

    def refund_charge(self, charge_id: int, data: dict) -> Any:
        """Refund a charge by its ID.

        Args:
            charge_id: ID of the charge
            data: dict with refund_amount and mark_only params.
            See API docs for more info

        Returns:
            A dictionary containing charge information, or an error
            message indicating what went wrong.
        """

        return self._post(str.format('/refund/charge/{0}', charge_id), data)

    def get_cards(self, customer_id: int) -> Any:
        """Get a list of cards associated with a customer.

        Args:
            customer_id: these can be obtained via get_customers()

        Returns:
            A list of dicts containing card information, or an error
            message indicating what went wrong.
        """

        return self._get(str.format('/cards/{0}', customer_id))

    def get_card(self, card_id: int) -> Any:
        """Get a single card by ID.

        Args:
            customer_id: these can be via get_customers()

        Returns:
            A list of dicts containing card information, or an error
            message indicating what went wrong.
        """

        return self._get(str.format('/card/{0}', card_id))

    def create_card(self, data: dict) -> Any:
        """Create a payment method and add it to an existing customer.

        Args:
            data: See docs linked in the header for param options.

        Returns:
            A dict containing card information, or an error
            message indicating what went wrong.
        """

        return self._post('/create/card', data)

    def delete_card(self, card_id: int) -> Any:
        """Delete an existing card by its ID number.

        Args:
            card_id: this can be found via the get_cards() method.

        Returns:
            A dictionary with {'status: 'success' or 'fail'}
            or an error message indicating what went wrong.
        """

        data = dict([('id', card_id)])
        return self._post('/delete/card', data)

    def get_promos(self) -> Any:
        """Return a list of all promos on file."""

        return self._get('/promo')

    def get_promo(self, promo_id: int) -> Any:
        """Get a single promo by ID.

        Args:
            promo_id: these can be obtained via get_customers()

        Returns:
            A dict containing promo information, or an error
            message indicating what went wrong.
        """

        return self._get(str.format('/promo/{0}', promo_id))

    def create_promo(self, data: dict) -> Any:
        """Create a promo code to use with subscriptions.

        Args:
            data: See docs linked in the header for param options.

        Returns:
            A dict containing promo information, or an error
            message indicating what went wrong.
        """

        return self._post('/create/promo', data)

    def delete_promo(self, promo_id: int) -> Any:
        """Delete an existing promo by its ID number.

        Args:
            promo_id: this can be found via the get_promos() method.

        Returns:
            A dictionary with {'status: 'success' or 'fail'}
            or an error message indicating what went wrong.
        """

        data = dict([('id', promo_id)])
        return self._post('/delete/promo', data)

    def get_email_template(self, template_id: int) -> Any:
        """Get the data for an email template when given an ID number.

        Args:
            template_id: Pass in a known template ID.
            You can find these on the paywhirl app template page.

        Returns:
            A dictionary containing information about the selected
            template, or an error message indicating what went wrong.
        """

        return self._get(str.format('/email/{0}', template_id))

    def send_email(self, data: dict) -> Any:
        """Send a system generated email based on one of your pre-
           defined templates on your paywhirl account page

        Args:
          see api.paywhirl.com, the list depends on what
          email templates you have available

        Returns:
          either a string with "status" => "success" or an error message indicating
          the need for another parameter
        """

        return self._post('/send-email', data)

    def get_account(self) -> Any:
        """Get a dictionary containing your account information."""

        return self._get('/account')

    def get_stats(self) -> Any:
        """Get invoice and revenue statistics about your account."""

        return self._get('/stats')

    def get_shipping_rules(self) -> Any:
        """Get a list of shipping rules in dict format."""

        return self._get('/shipping/')

    def get_shipping_rule(self, shipping_rule_id: int) -> Any:
        """Get the data for a shipping rule when given an ID number.

        Args:
            shipping_rule_id: Pass in a known template ID.
            You can find these using the get_shipping_rules() method.

        Returns:
            A dictionary containing information about the selected
            rule, or an error message indicating what went wrong.
        """

        return self._get(str.format('/shipping/{0}', shipping_rule_id))

    def get_tax_rules(self) -> Any:
        """Get a list of all tax rules created by your account."""

        return self._get('/tax')

    def get_tax_rule(self, rule_id: int) -> Any:
        """Get the data for a tax rule when given an ID number.

        Args:
            rule_id: Pass in a known tax rule ID.
            You can find these using the get_tax_rules() method.

        Returns:
            A dictionary containing information about the selected
            rule, or an error message indicating what went wrong.
        """

        return self._get(str.format('/tax/{0}', rule_id))

    def get_multi_auth_token(self, data: dict) -> Any:
        """Get a MultiAuth token to use to automatically
                login a customer to a widget.

        Args:
            data: See docs linked in the header for param options.

        Returns:
            A dict containing a multiauth token, or an error
            message indicating what went wrong.
        """
        return self._post('/multiauth', data)

    def _request(self, method: str, path: str, params: Any = None) -> Any:
        params = params or {}
        url = self._api_base + path
        headers = {'api_key': self._api_key, 'api_secret': self._api_secret}
        kwargs = {'headers': headers, 'verify': self._verify_ssl}

        if method == 'post':
            resp = requests.post(url, json=params, **kwargs)
        else:
            resp = requests.get(url, params=params, **kwargs)

        resp.raise_for_status()
        return resp.json()


    def _post(self, path: str, params: Any = None) -> Any:
        return self._request('post', path, params)

    def _get(self, path: str, params: Any = None) -> Any:
        return self._request('get', path, params)
