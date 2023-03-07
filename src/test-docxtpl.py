from docxtpl import DocxTemplate
import os

doc = DocxTemplate(os.getenv("HOME") +'/Downloads/demo.tpl.docx') # 读取模板
context = { 'company_name' : "World company" } # 需要传入的字典， 需要在word对应的位置输入 {{ company_name }}
doc.render(context) # 渲染到模板中
doc.save("generated_doc.docx") # 生成一个新的模板