responseLetterHeadingAndFooter = """<html>
    <body>
        <font face="TH Sarabun New">
        <center><img src = "components/cuEngLogo.jpg" width = "250"></center>
        <p style="text-align:center" ><font size = "4"><b>หนังสือรับมอบ
            <br/>โครงการหุ่นยนต์และอุปกรณ์​สนับสนุนการแพทย์ในสถานการณ์​โรคระบาด COVID-19​ (CU-RoboCovid)
            <br/>เพื่อพัฒนาหุ่นยนต์สำหรับให้ความช่วยเหลือบุคลากรทางการแพทย์
        </b></font></p>
        {0}
        <p>
            ชื่อโรงพยาบาลและหน่วยงานที่รับมอบ: {1}
        </p>
        <p style="text-align:right">
            <br/>
            <br/>ผู้อำนวยการ......................................................................
            <br/>(โปรดลงตราประทับหน่วยงาน)
        </p>
        <p>
        <b>หมายเหตุ</b>
        <ol type="1">
            <li> โปรดถ่ายรูปผู้รับมอบกับป้ายส่งมอบพร้อมอุปกรณ์ที่ท่านได้รับ</li>
            <li> ลงเซ็นชื่อรับโดยผู้อำนวยการหรือหัวหน้าหน่วยงานที่ได้รับมอบหมาย และ ลงตราประทับของหน่วยงาน</li>
            <li> โปรด Scan เอกสารนี้และส่งเอกสารพร้อมรูปถ่ายผ่านทาง QR Code ด้านล่าง และ ส่ง email มาที่ CU.Robocovid@gmail.com โดยใส่ในหัวเรื่องว่า “หนังสือรับมอบ_ชื่อโรงพยาบาล”</li>
            <li> จัดส่งเอกสารตัวจริงมาที่ “โครงการ CU-RoboCovid ห้อง MI Workspace ชั้น M อาคาร 100 ปี คณะวิศวกรรมศาสตร์ จุฬาลงกรณ์มหาวิทยาลัย 254 ถ.พญาไท วังใหม่ ปทุมวัน กทม. 10330 (080-292-3825)”</li>
        </ol>
        <table style="float:left;">
            <tr>
                <td>
                    <b>ขอขอบคุณมาอย่างสูง หากมีคำถามโปรดติดต่อที่</b>
                    <br/>รศ.ดร.วิทยา วัณณสุโภประสิทธิ์ 081-8449056
                    <br/>อาจารย์ ดร.สุรัฐ ขวัญเมือง 097-0521069
                </td>
            </tr>
        </table>
        <table style="float:right;">
            <tr>
                <td>
                    <img src = "components/hospitalReplyForm.svg" style = "width: 60px; height: 60px;">
                </td>
            <tr>
        </table>
        </p>
        </font>
    </body>
</html>"""

responseLetterBodyMirror = """
        <p>
            <b>เรื่อง</b> หนังสือรับมอบการสนับสนุน อุปกรณ์สื่อสารตรวจดูแลผู้ป่วยระยะไกลกับแพทย์ (Quarantine Tele-presence System)
        </p>
        <p>
            <b>เรียน</b> คณบดี คณะวิศวกรรมศาสตร์ จุฬาลงกรณ์มหาวิทยาลัย
        </p>
        <p>
            ตามที่คณะวิศวกรรมศาสตร์ได้ทำโครงการหุ่นยนต์และอุปกรณ์​สนับสนุนการแพทย์ในสถานการณ์​โรคระบาด COVID-19​ (CU-RoboCovid) เพื่อพัฒนาหุ่นยนต์สำหรับให้ความช่วยเหลือบุคลากรทางการแพทย์นั้น ทางโรงพยาบาลและหน่วยงานได้รับมอบอุปกรณ์สนับสนุนการแพทย์ดังนี้
        </p>
        <p>
            <ol type="1">
                <li>อุปกรณ์สื่อสารทางไกล “กระจก” (Quarantine Telepresence) ประกอบด้วย</li>
                <ol type="1">
                    <li>อุปกรณ์สื่อสารฝั่งของบุคลากรทางแพทย์ (Doctor Monitor) จำนวน {0} ชุด</li>
                    <li>อุปกรณ์สื่อสารฝั่งของผู้ป่วย (Patient Monitor) จำนวน {1} ชุด</li>
                </ol>
            </ol>
            จึงเรียนมาเพื่อขอขอบคุณเป็นอย่างสูง ณ โอกาสนี้
        </p>
"""

responseLetterBodyMirrorChaiPattana = """
        <p>
            <b>เรื่อง</b> หนังสือรับมอบการสนับสนุน อุปกรณ์สื่อสารตรวจดูแลผู้ป่วยระยะไกลกับแพทย์ (Quarantine Tele-presence System) พระราชทาน
        </p>
        <p>
            <b>เรียน</b> คณบดี คณะวิศวกรรมศาสตร์ จุฬาลงกรณ์มหาวิทยาลัย
        </p>
        <p>
            ทางโรงพยาบาลและหน่วยงานได้รับมอบอุปกรณ์สื่อสารตรวจดูแลผู้ป่วยระยะไกลกับแพทย์ (Quarantine Tele-presence System) พระราชทาน ดังนี้
        </p>
        <p>
            <ol type="1">
            <li>อุปกรณ์สื่อสารทางไกล “กระจก” (Quarantine Telepresence) ประกอบด้วย</li>
                <ol type="1">
                    <li>อุปกรณ์สื่อสารฝั่งของบุคลากรทางแพทย์ (Doctor Monitor) จำนวน {0} ชุด</li>
                    <li>อุปกรณ์สื่อสารฝั่งของผู้ป่วย (Patient Monitor) จำนวน {1} ชุด</li>
                </ol>
            </ol>
            จึงเรียนมาเพื่อขอขอบคุณเป็นอย่างสูง ณ โอกาสนี้
        </p>
"""

responseLetterBodyPinto = """
        <p>
            <b>เรื่อง</b> หนังสือรับมอบการสนับสนุน หุ่นยนต์ขนส่งในพื้นที่ติดเชื้อ “ปิ่นโต” (Pinto)
        </p>
        <p>
            <b>เรียน</b> คณบดี คณะวิศวกรรมศาสตร์ จุฬาลงกรณ์มหาวิทยาลัย
        </p>
        <p>
            ตามที่คณะวิศวกรรมศาสตร์ได้ทำโครงการหุ่นยนต์และอุปกรณ์​สนับสนุนการแพทย์ในสถานการณ์​โรคระบาด COVID-19​ (CU-RoboCovid) เพื่อพัฒนาหุ่นยนต์สำหรับให้ความช่วยเหลือบุคลากรทางการแพทย์นั้น ทางโรงพยาบาลและหน่วยงานได้รับมอบอุปกรณ์สนับสนุนการแพทย์ดังนี้
        </p>
        <p>
            <ol type="1">
                <li>หุ่นยนต์ขนส่งในพื้นที่ติดเชื้อ “ปิ่นโต” (Pinto) จำนวน {0} ชุด</li>
            </ol>
            จึงเรียนมาเพื่อขอขอบคุณเป็นอย่างสูง ณ โอกาสนี้
        </p>
"""

responseLetterBodyPintoChaiPattana = """
        <p>
            <b>เรื่อง</b> หนังสือรับมอบการสนับสนุน หุ่นยนต์ขนส่งในพื้นที่ติดเชื้อ “ปิ่นโต” (Pinto) พระราชทาน
        </p>
        <p>
            <b>เรียน</b> คณบดี คณะวิศวกรรมศาสตร์ จุฬาลงกรณ์มหาวิทยาลัย
        </p>
        <p>
            ทางโรงพยาบาลได้รับมอบหุ่นยนต์ขนส่งในพื้นที่ติดเชื้อ “ปิ่นโต” (Pinto) พระราชทาน จำนวน {0} ชุด เป็นที่เรียบร้อยแล้ว
        </p>
        <p>
            จึงเรียนมาเพื่อขอขอบคุณเป็นอย่างสูง ณ โอกาสนี้
        </p>
"""