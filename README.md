# 🎞 OSS project FinDrama
<br/>

## 📽 소개
<p>
  <img src='https://user-images.githubusercontent.com/69452161/118365322-2e0afc00-b5d7-11eb-892e-8db69ba46db9.png' width='200px'/>
</p>

### 방영중인 드라마의  정보를 확인해보세요
현재 방영중인 드라마의 리스트와 해당 드라마의 정보, 댓글들의 감정평가를 확인할 수 있습니다.
<br/>
<br/>

## 👷 팀원 정보 및 역할 분담
* 변효근 : 머신러닝 , Flask(Python) 
* 이준규 : 웹 디자인 , Flask(Python) 
* 이정은 : 데이터 수집(crawling), 데이터베이스 모델링 , Flask(Python) 
<br/>

## 🧰 기능
* 현재 방영중인 드라마 기본 정보 확인
* 드라마별 댓글 확인
* 댓글 감정 인식을 통한 드라마에 대한 평가 확인
* 드라마의 댓글을 통한 wordcloud 확인 가능
<br/>

## 📁 프로젝트 구조
![image](https://user-images.githubusercontent.com/69452161/119333969-80c67100-bcc5-11eb-905e-46a563c13bb9.png)
<br/>

```
Total
├─__pycache__  
│  ├─oss_database.cpython-37.pyc
│  └─oss_predict.cpython-37.pyc
├─templates 
│  ├─Static
│    ├─ css
│    └─ wordcloud
│  └─ html....
│
├─__init__.py
├─ oss.h5
├─ oss_database.py
├─ oss_predict.py
└─ oss_wordcloud.py
```
<br/>

## 💻 화면
![image](https://user-images.githubusercontent.com/69452161/119460638-dbb9a000-bd79-11eb-8df3-3a62f15a21ac.png)

<br/>

## :memo:데이터베이스 모델링

![image](https://user-images.githubusercontent.com/69452161/118365249-de2c3500-b5d6-11eb-877a-b52acd0954e0.png)
