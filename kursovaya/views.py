from django.http import HttpResponse
from django.shortcuts import render
import json
from django import forms
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


class NameForm(forms.Form):
    airport_id = forms.CharField(label='Airport_id', max_length=100)
    id = forms.CharField(label='ID', max_length=100)
    airline = forms.CharField(label='Airline', max_length=100)
    airplane = forms.CharField(label='Airplane', max_length=100)
    departure = forms.CharField(label='Departure', max_length=100)
    destination = forms.CharField(label='Destination', max_length=100)
    deptime = forms.CharField(label='Departure_time', max_length=100)
    destime = forms.CharField(label='Destination_time', max_length=100)


GROUP_CHOICES = (('Admin', 'Admin'), ('Users', 'Users'), ('Employees', 'Employees'))


class GroupForm(forms.Form):
    group = forms.ChoiceField(widget=forms.RadioSelect, choices=GROUP_CHOICES)
    username = forms.CharField(label='Username', max_length=100)


class UserForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    email = forms.CharField(label='Email', max_length=100)
    password = forms.CharField(label='Password', max_length=100)
    firstname = forms.CharField(label='First_name', max_length=100)
    lastname = forms.CharField(label='Last_name', max_length=100)

class AirportForm(forms.Form):
    number = forms.CharField(label='ID', max_length=100)
    name = forms.CharField(label='Name', max_length=100)
    country = forms.CharField(label='Country', max_length=100)
    city = forms.CharField(label='City', max_length=100)
    address = forms.CharField(label='Address', max_length=100)


class PassengerForm(forms.Form):
    airport_id = forms.CharField(label='Airport_id', max_length=100)
    flight_id = forms.CharField(label='Flight_id', max_length=100)
    lastname = forms.CharField(label='Lastname', max_length=100)
    firstname = forms.CharField(label='Firstname', max_length=100)
    secondname = forms.CharField(label='Secondname', max_length=100)
    gender = forms.CharField(label='Gender', max_length=100)
    birthdate = forms.CharField(label='Birthdate', max_length=100)
    nationality = forms.CharField(label='Nationality', max_length=100)


def airports_write_to_json(number, name, country, city, address):
    with open('data.json', 'r') as jfr:
        jf_file = json.load(jfr)
    with open('data.json', 'w') as jf:
        jf_target = jf_file['airports']
        flights_info = {'number': number, 'name': name, 'country': country, 'city': city, 'address': address, 'flights': []}
        jf_target.append(flights_info)
        json.dump(jf_file, jf, indent=2, ensure_ascii=False)


def write_to_json(airport_id, id, airline, airplane, departure, destination, deptime, destime):
    airport_id = int(airport_id)
    with open('data.json', 'r') as jfr:
        jf_file = json.load(jfr)
    with open('data.json', 'w') as jf:
        jf_target = jf_file['airports'][airport_id]['flights']
        flights_info = {'id': id, 'airline': airline, 'airplane': airplane, 'departure': departure, 'destination': destination, 'deptime': deptime, 'destime': destime, 'passengers': []}
        jf_target.append(flights_info)
        json.dump(jf_file, jf, indent=2, ensure_ascii=False)


def pass_write_to_json(id1, id2, lastname, firstname, secondname, gender, birthdate, nationality):
    id1 = int(id1)
    id2 = int(id2)
    with open('data.json', 'r') as jfr:
        jf_file = json.load(jfr)
    with open('data.json', 'w') as jf:
        jf_target = jf_file['airports'][id1]['flights'][id2]['passengers']
        flights_info = {'lastname': lastname, 'firstname': firstname, 'secondname': secondname, 'gender': gender, 'birthdate': birthdate, 'nationality': nationality}
        jf_target.append(flights_info)
        json.dump(jf_file, jf, indent=2, ensure_ascii=False)

def user_write_json(username, email, password, firstname, lastname):
    with open('users.json', 'r') as jfr:
        jf_file = json.load(jfr)
    with open('users.json', 'w') as jf:
        jf_target = jf_file['users']
        user_info = {'username': username, 'email': email, 'password': password, 'firstname': firstname, 'lastname': lastname, 'group': "Users"}
        jf_target.append(user_info)
        json.dump(jf_file, jf, indent=2, ensure_ascii=False)

def register(request):
    if request.method == 'POST':
        form2 = UserForm(request.POST)
        if form2.is_valid():
            username = form2.cleaned_data['username']
            email = form2.cleaned_data['email']
            password = form2.cleaned_data['password']
            firstname = form2.cleaned_data['firstname']
            lastname = form2.cleaned_data['lastname']
            user = User.objects.create_user(username, email, password)
            user.first_name = firstname
            user.last_name = lastname
            user_write_json(username, email, password, firstname, lastname)
            user.save()
            g = Group.objects.get(name="Users")
            g.user_set.add(user)
            return HttpResponseRedirect('/airports')
    else:
        form2 = UserForm()
    return render(request, 'airports.html', {'form': form2})


def input(request):
    if request.method == 'POST':
        form1 = NameForm(request.POST)
        if form1.is_valid():
            airport_id = int(form1.cleaned_data['airport_id'])
            id = form1.cleaned_data['id']
            airline = form1.cleaned_data['airline']
            airplane = form1.cleaned_data['airplane']
            departure = form1.cleaned_data['departure']
            destination = form1.cleaned_data['destination']
            deptime = form1.cleaned_data['deptime']
            destime = form1.cleaned_data['destime']
            write_to_json(airport_id, id, airline, airplane, departure, destination, deptime, destime)
            return HttpResponseRedirect('/airports')
    else:
        form1 = NameForm()
    return render(request, 'airports.html', {'form': form1})


def frs(request):
    if request.method == 'POST':
        form3 = PassengerForm(request.POST)
        if form3.is_valid():
            id1 = int(form3.cleaned_data['airport_id'])
            id2 = int(form3.cleaned_data['flight_id'])
            lastname = form3.cleaned_data['lastname']
            firstname = form3.cleaned_data['firstname']
            secondname = form3.cleaned_data['secondname']
            gender = form3.cleaned_data['gender']
            birthdate = form3.cleaned_data['birthdate']
            nationality = form3.cleaned_data['nationality']
            pass_write_to_json(id1, id2, lastname, firstname, secondname, gender, birthdate, nationality)
            return HttpResponseRedirect('/airports')
    else:
        form3 = UserForm()

    return render(request, 'airports.html', {'form': form3})


def emp_frs(request):
    if request.method == 'POST':
        form5 = PassengerForm(request.POST)
        if form5.is_valid():
            airport_id = int(form5.cleaned_data['airport_id'])
            flight_id = int(form5.cleaned_data['flight_id'])
            lastname = form5.cleaned_data['lastname']
            firstname = form5.cleaned_data['firstname']
            secondname = form5.cleaned_data['secondname']
            gender = form5.cleaned_data['gender']
            birthdate = form5.cleaned_data['birthdate']
            nationality = form5.cleaned_data['nationality']
            pass_write_to_json(airport_id, flight_id, lastname, firstname, secondname, gender, birthdate, nationality)
            return HttpResponseRedirect('/airports')

    return render(request, 'airports.html', {'form': form5})


def input_airports(request):
    if request.method == 'POST':
        form6 = AirportForm(request.POST)
        if form6.is_valid():
            number = form6.cleaned_data['number']
            name = form6.cleaned_data['name']
            country = form6.cleaned_data['country']
            city = form6.cleaned_data['city']
            address = form6.cleaned_data['address']
            airports_write_to_json(number, name, country, city, address)
            return HttpResponseRedirect('/airports')
        else:
            form6 = UserForm()

    return render(request, 'airports.html', {'form': form6})


def change_group(request):
    if request.method == 'POST':
        form9 = GroupForm(request.POST)
        if form9.is_valid():
            username = form9.cleaned_data['username']
            group = form9.cleaned_data['group']
            with open('users.json', 'r') as jfr:
                jf_file = json.load(jfr)
            with open('users.json', 'w') as jf:
                for j in range(len(jf_file['users'])):
                    if (str(jf_file['users'][j]['username']) == str(username)):
                        User.objects.all()
                        me = User.objects.get(username=username)
                        g = Group.objects.get(name=jf_file['users'][j]['group'])
                        g.user_set.remove(me)
                        my_group = Group.objects.get(name=group)
                        my_group.user_set.add(me)
                        jf_file['users'][j]['group'] = group
                        break
                json.dump(jf_file, jf, indent=2, ensure_ascii=False)
        return HttpResponseRedirect('/airports')
    else:
        form9 = UserForm()
    return render(request, 'airports.html', {'form': form9})


def zelolka(request):
    js = json.load(open('./data.json', encoding='windows-1251'))
    return render(request, 'zelolka.html', {'src': js})

def admin_panel(request):
    js = json.load(open('./users.json', encoding='windows-1251'))
    z = 0
    return render(request, 'admin_panel.html', {'src': js, 'pos':z})


def flights(request, number):
    js = json.load(open('./data.json', encoding='windows-1251'))
    x = int(number)
    z = 100000000
    lolka = js['airports']
    number = str(number)
    for i in range(len(js['airports'])):
        if (str(js['airports'][i]['number']) == number):
            z = i
            lolka = js['airports'][z]['flights']
    if (z == 100000000):
        return render(request, '404.html')
    return render(request, 'flights.html', {'src': js, 'z': lolka, 'temp': number, 'airport_id': z})


def passengers(request, airport_id, temp_flight_id):
    js = json.load(open('./data.json', encoding='windows-1251'))
    temp_flight_id = str(temp_flight_id)
    airport_id = int(airport_id)
    keker = js['airports']
    flight_id = 100000000
    for i in range(len(js['airports'][airport_id]['flights'])):
        if (str(js['airports'][airport_id]['flights'][i]['id']) == temp_flight_id):
            keker = js['airports'][airport_id]['flights'][i]['passengers']
            flight_id = i
            break
    if (flight_id == 100000000):
        return render(request, '404.html')
    return render(request, 'passengers.html', {'src': js, 'z': keker, 'airport_id': airport_id, 'flight_id': flight_id})


def airports(request):
    js = json.load(open('./data.json', encoding='windows-1251'))
    return render(request, 'airports.html', {'src': js})


def main(request):
    js = json.load(open('./data.json', encoding='windows-1251'))
    return render(request, 'main.html', {'src': js})


def flight_register(request, airport_id, temp_flight_id):
    temp_flight_id = str(temp_flight_id)
    airport_id = int(airport_id)
    js = json.load(open('./data.json', encoding='windows-1251'))
    for i in range(len(js['airports'][airport_id]['flights'])):
        if (str(js['airports'][airport_id]['flights'][i]['id']) == temp_flight_id):
            flight_id = i
    return render(request, 'flight_register.html', {'src': js, 'airport_id': airport_id, 'flight_id': flight_id})


def delete_flight(request, airport_id, flight_id):
    flight_id = str(flight_id)
    airport_id = int(airport_id)
    with open('data.json', 'r') as jfr:
        jf_file = json.load(jfr)
    with open('data.json', 'w') as jf:
            for j in range(len(jf_file['airports'][airport_id]['flights'])):
                if (str(jf_file['airports'][airport_id]['flights'][j]['id']) == flight_id):
                    del jf_file['airports'][airport_id]['flights'][j]
                    break
            json.dump(jf_file, jf, indent=2, ensure_ascii=False)
    return HttpResponseRedirect('/airports')


def delete_passenger(request, airport_id, flight_id, pass_lastname, pass_firstname, pass_secondname):
    flight_id = int(flight_id)
    airport_id = int(airport_id)
    pass_lastname = str(pass_lastname)
    pass_firstname = str(pass_firstname)
    pass_secondname = str(pass_secondname)
    with open('data.json', 'r') as jfr:
        jf_file = json.load(jfr)
    with open('data.json', 'w') as jf:
        for i in range(len(jf_file['airports'][airport_id]['flights'][flight_id]['passengers'])):
            if ((str(jf_file['airports'][airport_id]['flights'][flight_id]['passengers'][i]['lastname']) == pass_lastname) and (str(jf_file['airports'][airport_id]['flights'][flight_id]['passengers'][i]['firstname']) == pass_firstname) and (str(jf_file['airports'][airport_id]['flights'][flight_id]['passengers'][i]['secondname']) == pass_secondname)):
                del jf_file['airports'][airport_id]['flights'][flight_id]['passengers'][i]
                break
        json.dump(jf_file, jf, indent=2, ensure_ascii=False)
    return HttpResponseRedirect('/airports')


def delete_airport(request, airport_id):
    airport_id = str(airport_id)
    with open('data.json', 'r') as jfr:
        jf_file = json.load(jfr)
    with open('data.json', 'w') as jf:
        for i in range(len(jf_file['airports'])):
            if (str(jf_file['airports'][i]['number']) == airport_id):
                del jf_file['airports'][i]
                break
        json.dump(jf_file, jf, indent=2, ensure_ascii=False)
    return HttpResponseRedirect('/airports')


def airports_edit_page(request, airport_id):
    js = json.load(open('./data.json', encoding='windows-1251'))
    return render(request, 'airports_edit_page.html', {'src': js, 'airport_id': airport_id})


def airports_edit(request, airport_id):
    if request.method == 'POST':
        form6 = AirportForm(request.POST)
        if form6.is_valid():
            number = form6.cleaned_data['number']
            name = form6.cleaned_data['name']
            country = form6.cleaned_data['country']
            city = form6.cleaned_data['city']
            address = form6.cleaned_data['address']
            airport_id = str(airport_id)
            with open('data.json', 'r') as jfr:
                jf_file = json.load(jfr)
            with open('data.json', 'w') as jf:
                for i in range(len(jf_file['airports'])):
                    if (str(jf_file['airports'][i]['number']) == airport_id):
                        jf_file['airports'][i]['number'] = number
                        jf_file['airports'][i]['name'] = name
                        jf_file['airports'][i]['country'] = country
                        jf_file['airports'][i]['city'] = city
                        jf_file['airports'][i]['address'] = address
                        break
                json.dump(jf_file, jf, indent=2, ensure_ascii=False)
        else:
            form6 = UserForm()
    return HttpResponseRedirect('/airports')


def flights_edit_page(request, airport_id, flight_id):
    js = json.load(open('./data.json', encoding='windows-1251'))
    airport_id = int(airport_id)
    lolka = js['airports'][airport_id]['flights']
    return render(request, 'flights_edit_page.html', {'src': js, 'z': lolka, 'airport_id': airport_id, 'flight_id': flight_id})

def flights_edit(request, airport_id, flight_id):
    js = json.load(open('./data.json', encoding='windows-1251'))
    if request.method == 'POST':
        form1 = NameForm(request.POST)
        if form1.is_valid():
            airport_id = int(form1.cleaned_data['airport_id'])
            id = form1.cleaned_data['id']
            airline = form1.cleaned_data['airline']
            airplane = form1.cleaned_data['airplane']
            departure = form1.cleaned_data['departure']
            destination = form1.cleaned_data['destination']
            deptime = form1.cleaned_data['deptime']
            destime = form1.cleaned_data['destime']
            flight_id = str(flight_id)
            airport_id = int(airport_id)
            with open('data.json', 'r') as jfr:
                jf_file = json.load(jfr)
            with open('data.json', 'w') as jf:
                for j in range(len(jf_file['airports'][airport_id]['flights'])):
                    if (str(jf_file['airports'][airport_id]['flights'][j]['id']) == flight_id):
                        jf_file['airports'][airport_id]['flights'][j]['id'] = id
                        jf_file['airports'][airport_id]['flights'][j]['airline'] = airline
                        jf_file['airports'][airport_id]['flights'][j]['airplane'] = airplane
                        jf_file['airports'][airport_id]['flights'][j]['departure'] = departure
                        jf_file['airports'][airport_id]['flights'][j]['destination'] = destination
                        jf_file['airports'][airport_id]['flights'][j]['deptime'] = deptime
                        jf_file['airports'][airport_id]['flights'][j]['destime'] = destime
                        break
                json.dump(jf_file, jf, indent=2, ensure_ascii=False)
    else:
        form1 = NameForm()
    return HttpResponseRedirect('/airports')


def passengers_edit_page(request, airport_id, flight_id, pass_lastname, pass_firstname, pass_secondname):
    js = json.load(open('./data.json', encoding='windows-1251'))
    airport_id = int(airport_id)
    flight_id = int(flight_id)
    keker = js['airports'][airport_id]['flights'][flight_id]['passengers']
    return render(request, 'passengers_edit_page.html', {'src': js, 'z': keker, 'airport_id': airport_id, 'flight_id': flight_id, 'pass_lastname': pass_lastname, 'pass_firstname': pass_firstname, 'pass_secondname': pass_secondname})


def pass_edit(request, airport_id, flight_id, pass_lastname, pass_firstname, pass_secondname):
    if request.method == 'POST':
        form5 = PassengerForm(request.POST)
        if form5.is_valid():
            airport_id = int(airport_id)
            flight_id = int(flight_id)
            lastname = form5.cleaned_data['lastname']
            firstname = form5.cleaned_data['firstname']
            secondname = form5.cleaned_data['secondname']
            gender = form5.cleaned_data['gender']
            birthdate = form5.cleaned_data['birthdate']
            nationality = form5.cleaned_data['nationality']
            pass_lastname = str(pass_lastname)
            pass_firstname = str(pass_firstname)
            pass_secondname = str(pass_secondname)
            with open('data.json', 'r') as jfr:
                jf_file = json.load(jfr)
            with open('data.json', 'w') as jf:
                for i in range(len(jf_file['airports'][airport_id]['flights'][flight_id]['passengers'])):
                    if ((str(jf_file['airports'][airport_id]['flights'][flight_id]['passengers'][i]['lastname']) == pass_lastname) and (str(jf_file['airports'][airport_id]['flights'][flight_id]['passengers'][i]['firstname']) == pass_firstname) and (str(jf_file['airports'][airport_id]['flights'][flight_id]['passengers'][i]['secondname']) == pass_secondname)):
                        jf_file['airports'][airport_id]['flights'][flight_id]['passengers'][i]['lastname'] = lastname
                        jf_file['airports'][airport_id]['flights'][flight_id]['passengers'][i]['firstname'] = firstname
                        jf_file['airports'][airport_id]['flights'][flight_id]['passengers'][i]['secondname'] = secondname
                        jf_file['airports'][airport_id]['flights'][flight_id]['passengers'][i]['gender'] = gender
                        jf_file['airports'][airport_id]['flights'][flight_id]['passengers'][i]['birthdate'] = birthdate
                        jf_file['airports'][airport_id]['flights'][flight_id]['passengers'][i]['nationality'] = nationality
                        break
                json.dump(jf_file, jf, indent=2, ensure_ascii=False)
        else:
            form5 = PassengerForm()
    return HttpResponseRedirect('/airports')

