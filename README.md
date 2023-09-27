![image](https://github.com/zeonga1102/myojeong_BE/assets/71905164/3b84b2be-e22a-4e84-9110-5006fdc1a930)
# 🌕묘정 송편
⭐소원을 빌고 송편을 받자⭐ <br>
달나라에 사는 토끼 요정 묘정이가 특별한 송편을 만들어줍니다! <br>
나를 위해, 혹은 다른 사람을 위해 소원을 빌어보세요🙏<br>
# 🎑Intro
* 소원을 적고 다른 사람들과 공유 및 상호작용하는 웹 서비스
* 배포 완료
* **기간**: 2023. 09. 11 ~ 2023. 09. 27
* **개발 인원 (3명)**
  * Backend: 이정아
  * Frontend: 김채정, 이상민
# 🐰Project
### Front Repository
<a href="https://github.com/blcklamb/myojeong_fe/blob/develop/README.md"><img src="https://img.shields.io/badge/Github-000000?style=flat-square&logo=github&logoColor=white"/></a>
### 기술 스택
* Python 3.10
* Django 4.2
* Django Rest Framework 3.14
* PostgreSQL 14.9
* Nginx
* Gunicorn
* AWS EC2
### Feature
* SSL 적용, http 요청 시 https로 redirect
* Log file 저장
### 역할
* 기획
* DB 설계
* API 설계 및 구현
* 서버 배포
### Architecture
![image](https://github.com/zeonga1102/myojeong_BE/assets/71905164/d13c3af0-f0d8-47db-99f7-7daba76eecce)
# 🛠️Troubleshooting
### 1. SSL 인증서 발급
Let's Encrypt를 통해 인증서를 발급받고 https 통신이 가능하게 서버를 세팅하려고 했다.
우선 인증서 발급부터 문제가 있었다. 인증서 발급을 위한 명령어를 실행하는 도중 도메인을 입력하는 마지막 단계에서 에러가 발생했다.
```
The Certificate Authority failed to verify the temporary nginx configuration changes made by Certbot.
Ensure the listed domains point to this nginx server and that it is accessible from the internet.
```
방법을 찾아보다가 처음부터 certbot 설치부터 다시 시작했고 snapd를 설치한 후 재부팅을 하고 이후 과정을 수행하니 에러 없이 인증서가 잘 발급되었다.
단, 인증서를 발급하는 과정에서 인증 과정이 너무 많이 틀리면 아래와 같은 에러가 발생한다. 1시간 정도 후에 다시 시도해야한다.
```
An unexpected error occurred: Error creating new order :: too many failed authorizations recently:
see https://letsencrypt.org/docs/failed-validation-limit/
```
<details>
<summary>인증서 발급 과정</a></summary>

[Certbot 사이트](https://certbot.eff.org/instructions?ws=nginx&os=ubuntufocal)를 참고하여 명령어를 실행한다.
```
$ sudo apt update
$ sudo apt install snapd
// 재부팅!!
$ sudo reboot

$ sudo snap install core; sudo snap refresh core
$ sudo snap install -classic certbot
$ sudo ln -s /snap/bin/certbot /usr/bin/certbot
$ sudo certbot certonly --nginx
```
해당 명령어들이 실행 완료되면 /etc/letsecrypt/live/`도메인`/ 경로에 fullchain.pem, privkey.pem이 생성된다.<br>
이후 nginx 설정에 해당 파일들의 경로를 넣어줘야 한다.
</details>

### 2. HTTPS 적용
nginx에 대해서 아직 잘 모르다보니 설정을 잘못 해서 nginx가 실행이 안 됐었다.
```
server {
    listen 80;
    server_name myojeong.ddns.net;

    location / {
        return 301 https://$host$request_uri;
    }
}

server {
    listen 443 ssl http2;
    server_name myojeong.ddns.net;

    ssl_certificate /etc/letsencrypt/live/myojeong.ddns.net/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/myojeong.ddns.net/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:8000;
        include proxy_params;
    }

 }
```
`servier_name`에는 인증서를 발급받을 때 입력했던 도메인을 적는다. 그리고 `ssl_certificate`과 `ssl_certificate_key`에는 발급받은 key 파일의 경로를 적는다.<br>
http로 요청이 들어오면 https로 redirect를 시키기 위해 80번 포트의 location을 위와 같이 설정한다.<br>
중간에 테스트 서버는 http 요청에 대해서 redirect 하지 말아달라고 해서 해당 경로를 443 포트의 location과 동일하게 설정했었다.<br>
그리고 미처 생각 못하고 있다가 한참을 헤맸던건 443번 포트를 반드시 열어줘야 한다는 것이다.
https 통신을 443번 포트에서 하겠다고 설정을 했으니 당연히 443번 포트를 열어야 한다. ec2의 보안그룹을 수정하자.

### 3. psycopg2 설치 에러
로컬에서 설치할 때는 아무 문제가 없었는데 ec2 인스턴스의 파이썬 가상환경에서 설치하려니 아래와 같은 에러가 발생했다.
```
error: subprocess-exited-with-error
```
libpq-dev를 설치하고 다시 시도하니 설치 되었다. 해당 [문서](https://pypi.org/project/libpq-dev/)를 보니 psycopg2의 종속성이라고 한다.
```
sudo apt-get install libpq-dev
```

### 4. CORS 에러
이번 프로젝트를 하면서 마주했던 인프라 관련 에러 중에 가장 쉽게 해결했다.<br>
프론트와 백 서버가 분리되어 있다보니 프론트에서 API 요청을 보낼 때 CORS 에러가 발생했다. 우선 `django-cors-headers`를 설치한다.
```
pip install django-cors-headers
```
그 후 settings.py 파일을 수정한다.
<details>
<summary>settings.py</a></summary>

```
INSTALLED_APPS = [
	...
    'corsheaders'
]

...

# MIDLEWARE 상단에 추가
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    ...
]

...

# CORS 설정 - whitelist 에 추가된 주소 접근 허용
CORS_ORIGIN_WHITELIST = ['http://127.0.0.1:3000' ,'http://localhost:3000']
CORS_ALLOW_CREDENTIALS = True
```
</details>

# 🖋️회고
우선 좋은 사람들이랑 함께 프로젝트를 진행할 수 있어서 좋았다. 짧은 기간동안 진행해서 볼륨은 크지 않지만 재밌게 했다.
프로젝트 코드에서 도커와 도커 컴포즈를 보고 알 수 있듯이 사실 나는 이번 프로젝트를 하면서 다른 것보다 '무중단 배포'를 하는 것이 목표였다. 하지만 내가 직접 서버 세팅을 해서 배포를 해본 적도 없는데다가 짧은 기간 동안 많은 시간을 낼 수 있는 것도 아니어서 결국 하지 못했다.
도커는 정말 잘 모르겠다. 그래도 이전에 해보지 않은 nginx와 gunicorn을 이용한 ssl이 적용된 장고 어플리케이션을 배포하는데 성공해서 뿌듯하다.
그동안 인프라와 배포 과정을 굉장히 어렵다고 생각해서 피해왔는데 이번 기회를 통해 해볼 수 있어서 좋았다. 당연히 시간도 많이 쓰고 에러도 많이 겪었다.
대신 그만큼 다음번에는 더 빠르게 잘할 수 있을 것 같다. 그리고 프로젝트 진행 후에 배포 경험이 적은만큼 그동안 로그에 대해서도 신경을 안 쓰다시피 했는데 이번엔 로거를 이용해 로그 파일이 저장되도록 했다.<br>
무중단 배포를 하지 못한 것 외에도 아쉬운게 있다면 아직 인프라에 대한 지식이 부족해서 인스턴스와 서버 세팅을 무엇을 기준으로 어떻게 해야할지 잘 모르겠던 것과 DB를 인스턴스 로컬에 두고 쓴 것이다.
인스턴스는 우선 t2.micro로 설정해둔 상태인데 어느 정도의 사양이 적합한지는 잘 모르겠다. 지금은 사람들이 쓰기 시작할 때 모니터링을 해서 사양 조정을 하는게 필요할 수도 있을 것 같다.
DB는 RDS를 쓰고 싶긴 했다. 하지만 이것도 시간 문제로 못했다. 다음에는 꼭 해보도록 해야겠다. 여러 여건 상 넣고 싶었지만 넣지 못한 기능들, 해보고 싶었지만 하지 못한 것들이 있지만 그동안 하지 않았던 서버 세팅과 배포를 하면서 많은 공부가 됐다.<br>
내가 만든 프로젝트를 실제 사람들이 이용한 경험이 거의 없다시피 해서 곧 사람들이 묘정 송편을 사용하게 될게 너무 기대된다. 이왕 배포하는거니까 사람들이 많이 쓸 수록 좋을 것 같다ㅎㅎ
다들 너무 고생하셨어용!!!!
