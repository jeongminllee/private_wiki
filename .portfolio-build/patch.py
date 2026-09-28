from zipfile import ZipFile, ZIP_DEFLATED
from lxml import etree as E
from pathlib import Path
base=Path('D:/wiki/.portfolio-build')
source=Path('D:/wiki/raw/portfolio/이정민_포트폴리오.pptx')
ns={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
with ZipFile(source) as z, ZipFile(base/'authored.pptx') as authored:
    root=E.fromstring(z.read('ppt/slides/slide6.xml'))
    ar=E.fromstring(authored.read('ppt/slides/slide6.xml'))
    tree=root.find('p:cSld/p:spTree',ns)
    maxid=max(int(x.get('id')) for x in root.findall('.//p:cNvPr',ns))
    count=0
    for sh in ar.findall('.//p:spTree/p:sp',ns):
        nv=sh.find('p:nvSpPr/p:cNvPr',ns)
        if nv is not None and nv.get('name','').startswith('GUAM_PR213_'):
            count+=1;nv.set('id',str(maxid+count));tree.append(sh)
    assert count==8,count
    changes={'GPU-Based AutoML 오픈소스 프레임워크 개발':'GUAM — GPU 기반 AutoML 프레임워크 개발','Only GPU 를 지향하는 AutoML 프레임워크':'LightAutoML 구조를 RAPIDS로 포팅하는 팀 프로젝트 · 비공개 알파','05  /  FrameWork Development':'05  /  FRAMEWORK DEVELOPMENT'}
    for text in root.findall('.//a:t',ns):
        if text.text in changes:text.text=changes[text.text]
    for sh in root.findall('.//p:sp',ns):
        if ''.join(sh.xpath('.//a:t/text()',namespaces=ns))=='프레임워크 개발':
            for num in sh.findall('.//a:buAutoNum',ns):num.set('startAt','2')
    notes=E.fromstring(z.read('ppt/notesSlides/notesSlide6.xml'))
    for sh in notes.findall('.//p:sp',ns):
        ph=sh.find('p:nvSpPr/p:nvPr/p:ph',ns)
        if ph is not None and ph.get('type')=='body':
            tx=sh.find('p:txBody',ns)
            for para in tx.findall('a:p',ns):tx.remove(para)
            for line in ['출처: https://github.com/ModulabsRAPIDSLAB/GUAM/pull/213', '[DOC-05] 2026-08-19 저장소 문서 정합성 감사 (JEY-225). 작성자 jeongminllee. 2026-09-01 병합.', '병합 커밋: 71402104961eaef3dea24f8f93f385f30be1143a. PR HEAD: cc3e321f1c4037c966e49183bdfc50dc79cc5670.', '최종 병합 diff: 31개 파일, 380줄 추가, 143줄 삭제. 코드 변경은 주석·docstring이며 기능 구현 실적으로 제시하지 않는다.', '비GPU 테스트 1,595개 통과는 PR 본문의 2026-08-25 검증 기록이다. 최종 병합 HEAD에 대한 이번 재실행 결과가 아니며 GPU 성능 검증을 뜻하지 않는다.']:
                para=E.SubElement(tx,'{'+ns['a']+'}p');run=E.SubElement(para,'{'+ns['a']+'}r');E.SubElement(run,'{'+ns['a']+'}t').text=line
    edits={'ppt/slides/slide6.xml':E.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True),'ppt/notesSlides/notesSlide6.xml':E.tostring(notes,xml_declaration=True,encoding='UTF-8',standalone=True)}
    with ZipFile(base/'candidate.pptx','w',ZIP_DEFLATED) as out:
        for info in z.infolist():out.writestr(info,edits.get(info.filename,z.read(info.filename)))
with ZipFile(source) as z,ZipFile(base/'candidate.pptx') as out:
    changed=[n for n in z.namelist() if z.read(n)!=out.read(n)]
    assert set(changed)==set(edits),changed
    print('Only changed:',changed)
    print('Size:',E.fromstring(z.read('ppt/presentation.xml')).find('p:sldSz',ns).attrib)
