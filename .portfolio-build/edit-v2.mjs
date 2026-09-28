import fs from 'node:fs/promises';
import {FileBlob,PresentationFile} from '@oai/artifact-tool';
const p=await PresentationFile.importPptx(await FileBlob.load('D:/wiki/raw/portfolio/이정민_포트폴리오.pptx'));
const s=p.slides.getItem(5);
function add(name,text,y,size,color='#1B3047',bold=false,h=60,fill='none'){
 const sh=s.shapes.add({name:'GUAM_PR213_'+name,geometry:'textbox',position:{left:985,top:y,width:830,height:h},fill,line:{fill:'none',width:0}});
 sh.text=text;sh.text.style={typeface:'Noto Sans Kr',fontSize:size,color,bold,autoFit:'none'};
}
add('lead','코드와 문서의 불일치를 실제로 정정',351,36,'#1B3047',true,60);
add('scope','PR #213 실제 변경 전후 · docs/API-SPEC.md',419,25,'#3165A9',false,50);
add('example1','사용 안내: 목표 API와 실행 가능한 예제 구분',479,27,'#1B3047',true,48);
add('before1','− 아래는 GUAM이 완성되었을 때의\n   목표 사용자 API이다.',531,26,'#9C343B',false,82,'#FFF0EF');
add('after1','+ 아래는 현재 공개된 TabularAutoML 기본 프리셋의\n   GPU 실행 예제다.',619,26,'#216347',false,82,'#ECF6EF');
add('after2','+ GPU 런타임과 선택한 알고리즘 모듈이\n   준비되어 있어야 실행할 수 있다.',701,26,'#216347',false,82,'#ECF6EF');
add('example2','모듈 상태: RandomForestGPU',800,27,'#1B3047',true,48);
add('before2','− stub (ML-04에서 구현)',848,25,'#9C343B',false,44,'#FFF0EF');
add('after3','+ 구현 완료 (guam/ml_algo/random_forest.py)',892,25,'#216347',false,44,'#ECF6EF');
add('result','31개 파일 정비 · 2026.09.01 PR 병합 완료',954,26,'#3165A9',true,47);
await (await PresentationFile.exportPptx(p)).save('D:/wiki/.portfolio-build/authored-v2.pptx');
console.log('Evidence excerpts authored');
