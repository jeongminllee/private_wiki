import fs from 'node:fs/promises';
import {FileBlob,PresentationFile} from '@oai/artifact-tool';
const p=await PresentationFile.importPptx(await FileBlob.load('D:/wiki/assets/portfolio/이정민_포트폴리오_GUAM기여추가.pptx'));
for(let i=0;i<6;i++){
 const png=await p.slides.getItem(i).export({format:'png',scale:0.5});
 await fs.writeFile(`D:/wiki/.portfolio-build/final-${i+1}.png`,new Uint8Array(await png.arrayBuffer()));
}
const montage=await p.export({format:'png',montage:true,scale:0.35});
await fs.writeFile('D:/wiki/.portfolio-build/final-montage.png',new Uint8Array(await montage.arrayBuffer()));
console.log('All six slides rendered');
