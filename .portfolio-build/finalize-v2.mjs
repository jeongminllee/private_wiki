import fs from 'node:fs/promises';
import {FileBlob,PresentationFile} from '@oai/artifact-tool';
import {finalizePresentation} from 'file:///C:/Users/AI-00/.codex/plugins/cache/openai-primary-runtime/presentations/26.909.61513/skills/presentations/container_tools/artifact_tool_utils.mjs';
const root='D:/wiki';
const sk='C:/Users/AI-00/.codex/plugins/cache/openai-primary-runtime/presentations/26.909.61513/skills/presentations';
const p=await PresentationFile.importPptx(await FileBlob.load(root+'/.portfolio-build/candidate-v2.pptx'));
const s=p.slides.getItem(5);
const blob=await s.export({format:'png',scale:1});
await fs.writeFile(root+'/.portfolio-build/after-v2.png',new Uint8Array(await blob.arrayBuffer()));
console.log('Preview rendered');
const result=await finalizePresentation({workspaceDir:root,candidatePath:root+'/.portfolio-build/candidate-v2.pptx',finalPath:root+'/assets/portfolio/이정민_포트폴리오_GUAM실제변경사례.pptx',pythonExecutable:'C:/Users/AI-00/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe',integrityValidatorPath:sk+'/container_tools/inspect_presentation_package_integrity.py',layoutValidatorPath:sk+'/container_tools/inspect_presentation_layout_geometry.py',layoutArgs:['--expected-slide-size-emu','18288000,10287000','--validate-bullet-geometry','--validate-heading-fit'],explicitTotalSlideCount:6,verifyArtifactToolImport:true,receiptPath:root+'/.portfolio-build/validation-v2.json'});
console.log(JSON.stringify(result));


