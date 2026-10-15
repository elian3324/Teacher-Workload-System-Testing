import {fileURLToPath} from 'node:url';
import fs from 'node:fs/promises';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';
const wb=Workbook.create(); const sh=wb.worksheets.add('Sheet1');
sh.getRange('A1:N4').values=[['Course Code','Course Instructor','Section','Class Nbr','Course Title','Employee ID','Course Units','Course Component','Medium of Instruction','Days&Time','Term','Graded Component','Total Enroll','Actual Enrol'],['QATEST101','QA1014模拟教师','QAA','991401','QA1014_1139标准课时模拟','QA1014T',3,'LEC','English','Mon 10:30 - 12:20','2710','LEC',20,20],['QATEST102','QA1014模拟教师','QAB','991402','QA1014_1139缺失时间模拟','QA1014T',3,'LEC','English','','2710','LEC',10,10],['QATEST103','QA1014模拟教师','QAC','991403','QA1014_1139零学分模拟','QA1014T',0,'TUT','English','Tue 14:00 - 14:50','2710','LEC',5,5]];
sh.showGridLines=false; sh.getRange('A1:N4').format.font={name:'Arial',size:11}; sh.getRange('A1:N1').format.font.bold=true; sh.getRange('A1:N4').format.autofitColumns(); sh.getRange('A1:N4').format.rowHeight=24;
wb.recalculate(); console.log((await wb.inspect({kind:'table',range:'Sheet1!A1:N4',tableMaxRows:4,tableMaxCols:14})).ndjson);
const img=await wb.render({sheetName:'Sheet1',range:'A1:N4',scale:1,format:'png'}); await fs.writeFile(new URL('./SIS模拟数据预览.png',import.meta.url),new Uint8Array(await img.arrayBuffer()));
await (await SpreadsheetFile.exportXlsx(wb)).save(fileURLToPath(new URL('./CUSZ_CRSE_SUMMARY_PG QA1014_1139 Term.xlsx',import.meta.url)));


const hw=Workbook.create(); const hs=hw.worksheets.add('TIME_INSTRUCTOR'); hs.getRange('A1:J3').values=[['Class Date','Class','Title','Instructor','Days&Time','Room','Role','Enrolled','Term','Class Nbr'],['2027-09-06','QAT 1101-L01(991401)','QA1014_1139标准课时模拟','QA1014模拟教师','Mon 10:30 - 12:20','QA1014','PI',20,'2710','991401'],['2027-09-07','QAT 1103-T01(991403)','QA1014_1139零学分模拟','QA1014模拟教师','Tue 14:00 - 14:50','QA1014','PI',5,'2710','991403']]; hs.getRange('A1:J3').format.autofitColumns(); hw.recalculate(); await (await SpreadsheetFile.exportXlsx(hw)).save(fileURLToPath(new URL('./TIME_INSTRUCTOR_QA1014_1139.xlsx',import.meta.url)));



