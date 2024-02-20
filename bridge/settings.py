"""
Django settings for bridge project.

Generated by 'django-admin startproject' using Django 3.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib import Path

import pymysql
pymysql.install_as_MySQLdb()
from requests.adapters import HTTPAdapter, Retry

from datetime import datetime
import requests
import time
import json

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-mn1(um@%7zpkq2vi#yh^3&yx*q(asx9!dshy@=3qxkj!@@392_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*", "103.107.67.160"]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'bridge',
    'corsheaders',
    'Appsetting',
    'Lead',
    'Employee',
    'DeliveryNote',
    'Company',
    'Branch',
    'Opportunity',
    'BusinessPartner',
    'Demo',
    'Activity',
    'Countries',
    'Industries',
    'PaymentTermsTypes',
    'Item',
    'Quotation',
    'Order',
    'Invoice',
    'Notification',   
    'Campaign',
    'Attachment',
    'SmtpSetting',
    'Expense',
    'Payment',
    'Delivery',
    'DiscountPolicy',
    'Pagination',
    'JournalEntries',
    'Warehouse',
    'TripExpenses',
    'PurchaseOrders',
    'PurchaseInvoices',
    'PurchaseDeliveryNotes',
]

# Use Django's standard `django.contrib.auth` permissions,
# or allow read-only access for unauthenticated users.

# REST_FRAMEWORK = {
    # 'DEFAULT_PERMISSION_CLASSES': [
      #'rest_framework.permissions.IsAuthenticated',
        # 'rest_framework.permissions.AllowAny'
    # ]
# }

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware'
]

ROOT_URLCONF = 'bridge.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'bridge.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
"""

import pymysql
pymysql.install_as_MySQLdb()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ledure_dev',
        'USER': 'root',
        'PASSWORD': 'root',
        # 'PASSWORD': 'F5GB?d4R#SW@r',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True

CORS_ORIGIN_ALLOW_ALL = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# STATIC_URL = '/static/'
STATIC_URL = '/static/'  # The URL prefix for static files.
STATIC_ROOT = os.path.join(BASE_DIR, 'static')  # The directory where collected static files will be stored.


SAPURL = 'https://35.154.67.167:50000/b1s/v1'
# SAPURL = 'https://analytics103u.uneecloud.com:50000/b1s/v1'

# <><><><><><><>><><><><><><>><><><><><<><><>><><><><><<
# <><><><><><><>SAP Database Connection><>><><><><><<><>
# <><><><><><><>><><><><><><>><><><><><<><><>><><><><><<


def SAPSESSION(inp):
    if inp =="api":
        file = "bridge/db.json"
    else:
        file = "../bridge/db.json"
    with open(file) as f:
        db = f.read()
        data = json.loads(db)

    now = datetime.today()
    current_dtime = now.strftime("%Y-%m-%d %H:%M:%S")
    
    d1 = datetime.strptime(data['at'], '%Y-%m-%d %H:%M:%S')
    d2 = datetime.strptime(current_dtime, '%Y-%m-%d %H:%M:%S')

    diff = d2 - d1

    diff_minutes = (diff.days * 24 * 60) + (diff.seconds/60)
    #diff_minutes = diff_minutes+30

    print(int(diff_minutes))
    if diff_minutes < 5:
        #print("valid")
        return data
    else:
        #print("session expire")
        """ old
        ses = requests.post(data['sapurl']+'/Login', data=json.dumps(data), verify=False)
        ses_json = json.loads(ses.text)
        """
        requestSession = requests.Session()
        retry = Retry(total=5, connect=5, backoff_factor=0.5)
        print(retry)
        adapter = HTTPAdapter(max_retries=retry)
        print(adapter)
        requestSession.mount('http://', adapter)
        requestSession.mount('https://', adapter)
        ses = requestSession.post(data['sapurl']+'/Login', data=json.dumps(data), verify=False)
        print(ses)
        ses_json = json.loads(ses.text)
        
        #print("new ses id"+ses_json['SessionId'])
        #print("old data")
        #print(data)
        data['SessionId'] = ses_json['SessionId']
        data['at'] = current_dtime
        
        #print("new data")
        #print(data)
        f = open(file, "w")
        f.write(json.dumps(data))
        f.close()
        return data
        
def SAPSESSIONNEW(inp):
    if inp =="api":
        file = "bridge/db.json"
    else:
        file = "../bridge/db.json"
    with open(file) as f:
        db = f.read()
        data = json.loads(db)

    print("SAP DB details",data)
    now = datetime.today()
    current_dtime = now.strftime("%Y-%m-%d %H:%M:%S")
    
    d1 = datetime.strptime(data['at'], '%Y-%m-%d %H:%M:%S')
    d2 = datetime.strptime(current_dtime, '%Y-%m-%d %H:%M:%S')

    diff = d2 - d1

    diff_minutes = (diff.days * 24 * 60) + (diff.seconds/60)
    #diff_minutes = diff_minutes+30

    session = requests.session()
    print(int(diff_minutes))
    if diff_minutes < 25:
        #print("valid")
        session.cookies.set('B1SESSION', data['SessionId'], path='/', domain='35.154.67.167')
        #return data
        return session

    else:        
        requestSession = requests.Session()
        retry = Retry(total=5, connect=5, backoff_factor=0.5)
        print(retry)
        adapter = HTTPAdapter(max_retries=retry)
        print(adapter)
        requestSession.mount('http://', adapter)
        requestSession.mount('https://', adapter)
        ses = requestSession.post(data['sapurl']+'/Login', data=json.dumps(data), verify=False)
        print(ses.text)
        
        ses_json = json.loads(ses.text)
        session.cookies.set('B1SESSION', ses_json['SessionId'], path='/', domain='35.154.67.167')
        data['SessionId'] = ses_json['SessionId']
        data['at'] = current_dtime
        
        #print("new data")
        #print(data)
        f = open(file, "w")
        f.write(json.dumps(data))
        f.close()
        #return data
        return session    


def CALLAPI(method,apiurl,calltype,data):
        ses = SAPSESSIONNEW(calltype)
        requestSession = requests.Session()
        retry = Retry(total=5, connect=5, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        requestSession.mount('http://', adapter)
        requestSession.mount('https://', adapter)
        # <><><><><><<><><><><><><><><><><><><><><><><><><><>
        # <><><><><><<><><><><><><><><><><><><><><><><><><><>
        print("Session Cookies:", ses.cookies)
        if method == "post" and data !="":
            res = requestSession.post(SAPURL+apiurl, data=json.dumps(data), cookies=ses.cookies, verify=False)
        elif method == "post" and data =="":
            res = requestSession.post(SAPURL+apiurl, cookies=ses.cookies, verify=False)
        elif method == "patch":
            res = requestSession.patch(SAPURL+apiurl, data=json.dumps(data), cookies=ses.cookies, verify=False)
        elif method == "delete":
            res = requestSession.delete(SAPURL+apiurl, cookies=ses.cookies, verify=False)
        else:
            res = requestSession.get(SAPURL+apiurl, cookies=ses.cookies, verify=False)
        #ses_json = json.loads(ses.text)
        return res

def NONE(inp):
	if type(inp)!=int:
		return 0;
	else:
		return inp
