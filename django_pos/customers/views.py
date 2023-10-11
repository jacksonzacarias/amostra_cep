from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Customer


@login_required(login_url="/accounts/login/")
def CustomersListView(request):
    context = {
        "active_icon": "customers",
        "customers": Customer.objects.all()
    }
    return render(request, "customers/customers.html", context=context)


@login_required(login_url="/accounts/login/")
def CustomersAddView(request):
    context = {
        "active_icon": "customers",
    }

    if request.method == 'POST':
        # Save the POST arguements
        data = request.POST

        attributes = {
            "first_name": data['first_name'],
            "last_name": data['last_name'],
            "address": data['address'],
            "email": data['email'],
            "phone": data['phone'],
        }

        # Check if a customer with the same attributes exists
        if Customer.objects.filter(**attributes).exists():
            messages.error(request, 'Cliente já existente!',
                           extra_tags="warning")
            return redirect('customers:customers_add')

        try:
            # Create the customer
            new_customer = Customer.objects.create(**attributes)

            # If it doesn't exists save it
            new_customer.save()

            messages.success(request, 'Cliente: ' + attributes["first_name"] + " " +
                             attributes["last_name"] + ' criado com sucesso!', extra_tags="success")
            return redirect('customers:customers_list')
        except Exception as e:
            messages.success(
                request, 'Houve um erro durante a criação!', extra_tags="danger")
            print(e)
            return redirect('customers:customers_add')

    return render(request, "customers/customers_add.html", context=context)


@login_required(login_url="/accounts/login/")
def CustomersUpdateView(request, customer_id):
    """
    Args:
        customer_id : The customer's ID that will be updated
    """

    # Get the customer
    try:
        # Get the customer to update
        customer = Customer.objects.get(id=customer_id)
    except Exception as e:
        messages.success(
            request, 'Houve um erro ao selecionar o cliente!', extra_tags="danger")
        print(e)
        return redirect('customers:customers_list')

    context = {
        "active_icon": "customers",
        "customer": customer,
    }

    if request.method == 'POST':
        try:
            # Save the POST arguements
            data = request.POST

            attributes = {
                "first_name": data['first_name'],
                "last_name": data['last_name'],
                "address": data['address'],
                "email": data['email'],
                "phone": data['phone'],
            }

            # Check if a customer with the same attributes exists
            if Customer.objects.filter(**attributes).exists():
                messages.error(request, 'Cliente já existente!',
                               extra_tags="warning")
                return redirect('customers:customers_add')

            # Get the customer to update
            customer = Customer.objects.filter(
                id=customer_id).update(**attributes)

            customer = Customer.objects.get(id=customer_id)

            messages.success(request, '¡Cliente: ' + customer.get_full_name() +
                             ' atualizado com sucesso!', extra_tags="success")
            return redirect('customers:customers_list')
        except Exception as e:
            messages.success(
                request, 'Houve um erro durante the update!', extra_tags="danger")
            print(e)
            return redirect('customers:customers_list')

    return render(request, "customers/customers_update.html", context=context)


@login_required(login_url="/accounts/login/")
def CustomersDeleteView(request, customer_id):
    """
    Args:
        customer_id : The customer's ID that will be deleted
    """
    try:
        # Get the customer to delete
        customer = Customer.objects.get(id=customer_id)
        customer.delete()
        messages.success(request, '¡Cliente: ' + customer.get_full_name() +
                         ' apagado!', extra_tags="success")
        return redirect('customers:customers_list')
    except Exception as e:
        messages.success(
            request, 'Houve um erro durante a eliminação!', extra_tags="danger")
        print(e)
        return redirect('customers:customers_list')
