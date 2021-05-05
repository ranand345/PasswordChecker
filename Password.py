from flask import Flask, render_template, request, redirect
import requests
import hashlib
import sys

app = Flask(__name__)
print(__name__)

@app.route('/')
def my_home():
    return render_template('./index.html')

@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)

def write_to_file(data):
     with open('database.txt',  mode='a') as database:
         email = data["email"]
         subject= data["subject"]
         message=data["message"]
         file = database.write(f'\n{email}, {subject}, {message}')


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method =='POST':
        data = request.form.to_dict()
        write_to_file(data)
        return redirect('/thanks.html')
    else:
        return 'something wrong'

@app.route('/finding', methods=['POST', 'GET'])
def finding():
    if request.method == 'POST':
        data1 = request.form["inppassword"]
        check_password(data1)
    return {inppassword}
def request_api_data(query_char):
    url= 'https://api.pwnedpasswords.com/range/' + query_char
    res= requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error Handling: {res.staus_code},check the code')
    return res

def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h,count in hashes:
        if h == hash_to_check:
            return count
    return 0

def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    print(response)
    return get_password_leaks_count(response, tail)

def check_password(pass1):
    for password in pass1:
        count = pwned_api_check(password)
        if count:
            html = """
            <text> your password {password} was found {count} times .... Change it </text>
            """
            # print(f'{password} was found {count} times... Change your passsword')
        else:
            html = """
            <text> your password {password} was found {count} times. You are safe </text>
            """
            # print(f'{password} not found..')
    return 'done'

# def main(args):
#     for password in args:
#         count = pwned_api_check(password)
#         if count:
#             print(f'{password} was found {count} times... Change your passsword')
#         else:
#             print(f'{password} not found..')
#     return 'done'
    
# if __name__ == '__main__':
#     main(sys.argv[1:])



