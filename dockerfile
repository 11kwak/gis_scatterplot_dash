# 부모 이미지:버전, slim은 보통 최소화 버전 
FROM python:3.6.9

# dockerfile이 있는 곳에서 어떤 파일을 WORKDIR에 복사해놓겠다.(보통 환경설정을 가져갑니다. package.json, requirements.txt 등)
# package.json . = 현재경로의 package.json을 가져갑니다. # . . 현재경로의 모든 파일을 가져갑니다. 
COPY ./ ./ 

# requirements.txt 를 설치하겠다.(환경세팅을 해주겠다)
RUN pip3 install -r requirements.txt

# work directory 설정
WORKDIR /

# 8050 포트로 열어주겠다.
EXPOSE 8050

# 웹 서버 구동하는 명령어 
CMD ["python","./app.py"]

