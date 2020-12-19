import requests, lxml.html
from bs4 import BeautifulSoup

def login(empCode, pwd):
    with requests.Session() as sess:
        form = get_hiddenfields(sess,'https://itapps.ensureservices.in/EmployeePortal/loginpage.aspx')
        form['txtEmpcode']=empCode
        form['txtpwd']=pwd
        form['ImageButton1.x']='21'
        form['ImageButton1.y']='11'
        response = sess.post('https://itapps.ensureservices.in/EmployeePortal/loginpage.aspx',data=form)
        return sess

def get_hiddenfields(sess, url):
    login = sess.get(url)
    login_html = lxml.html.fromstring(login.text)
    hidden_inputs = login_html.xpath(r'//form//input[@type="hidden"]')
    form = {x.attrib["name"]: x.attrib["value"] for x in hidden_inputs}
    return form

if __name__ == '__main__':
    sess = login('ADMIN', 'ESSIL@1718')
    form = get_hiddenfields(sess,'https://itapps.ensureservices.in/EmployeePortal/UserEmailidUpdation.aspx')
    form['ctl00$ContentPlaceHolder1$Btnviewstatus'] = 'Get Details'
    for empCode in ['12338','10002']:
        form['ctl00$ContentPlaceHolder1$txtEmpcode'] = empCode
        email_page = sess.post('https://itapps.ensureservices.in/EmployeePortal/UserEmailidUpdation.aspx', data=form)
        soup = BeautifulSoup(email_page.content,'html.parser')
        html = lxml.html.fromstring(email_page.text)
        form_input = html.xpath(r'//form//input[@id="ContentPlaceHolder1_txtPassword"]')[0]
        password = form_input.attrib["value"]
        print(empCode, password)

    #print(soup.findAll('tr')[5].findAll('td')[1].find('input')['value'])
