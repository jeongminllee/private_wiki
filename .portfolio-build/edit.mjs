import fs from 'node:fs/promises';
import {FileBlob,PresentationFile} from '@oai/artifact-tool';
const p=await PresentationFile.importPptx(await FileBlob.load('D:/wiki/raw/portfolio/이정민_포트폴리오.pptx'));
const s=p.slides.getItem(5);
function add(name,text,y,size,color='#1B3047',bold=false,h=60){
 const sh=s.shapes.add({name:'GUAM_PR213_'+name,geometry:'textbox',position:{left:985,top:y,width:830,height:h},fill:'none',line:{fill:'none',width:0}});
 sh.text=text; sh.text.style={typeface:'Noto Sans Kr',fontSize:size,color,bold,autoFit:'none'};
}
add('lead','기술 문서 정합성 감사 및 최신화',351,38,'#1B3047',true,62);
add('scope','README · API 명세 · 아키텍처 · 코드 주석\n총 31개 파일을 코드·테스트·이슈 상태와 대조해 정비',421,28,'#617184',false,90);
add('work1','기본 OOF·블렌딩과 멀티레벨 스태킹 구분',544,30,'#1B3047',true,49);
add('detail1','기본 프리셋의 동작과 고급 API의 조립 경로 명확화',596,26,'#617184',false,46);
add('work2','구현 상태와 지원 범위 정정',660,30,'#1B3047',true,49);
add('detail2','오래된 stub 표기 수정 · 분산 기능의 제약 문서화\nCode ID·파일·Linear 연결 보완',712,26,'#617184',false,89);
add('result','PR #213 병합 완료',832,35,'#3165A9',true,60);
add('evidence','2026.09.01 병합 · +380 / −143줄\nPR 검증 기록: 비GPU 테스트 1,595개 통과',891,25,'#617184',false,90);
await (await PresentationFile.exportPptx(p)).save('D:/wiki/.portfolio-build/authored.pptx');
console.log('Authored native text boxes');
