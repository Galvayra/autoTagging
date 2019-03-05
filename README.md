#) KIST ontology automatic tagging


1) preprocessing.py

전사데이터의 수동태깅된 데이터를 이용하여 키워드 온톨로지 사전 및 벡터 문맥 사전 등을 구축
반드시 variables.py 의 PreProcessing option을 True로 해야함



2) filling.py

전사데이터의 자동태깅 대상 키워드의 온톨로지를 자동 태깅
do_test option을 True로 설정하면 1:N keyword에 대하여 10번째 발견할 때마다 테스트 문장으로 추출
반드시 variables.py 의 PreProcessing option을 False로 해야함



3) tagging.py

JSON 형식의 데이터를 입력 시 자동으로 태깅하여 결과를 반환
반드시 variables.py 의 PreProcessing option을 False로 해야함



4) test_1_N.py

filling.py 에서 추출된 test csv 데이터에 대한 자동 태깅
본 자동 태깅 시스템의 성능을 평가하기 위한 스크립트
반드시 variables.py 의 PreProcessing option을 False로 해야함
