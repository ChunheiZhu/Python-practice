import os
import json
import numpy as np
from datasets import load_dataset, Dataset
import torch
from transformers import AutoTokenizer, AutoModel, Trainer, TrainingArguments, logging
from peft import get_peft_model, LoraConfig, TaskType, PeftModel
import uuid

logging.set_verbosity_error()

print("Loading ChatGLM2 ...")

if torch.cuda.is_available():
    print("GPU is available.")
    print(f"Current device: {torch.cuda.current_device()}")
    print(f"Device name: {torch.cuda.get_device_name(torch.cuda.current_device())}")
else:
    print("GPU is NOT available. Please check your CUDA installation.")
    print("Falling back to CPU, which will be much slower.")

tokenizer = AutoTokenizer.from_pretrained("THUDM/chatglm2-6b", trust_remote_code=True)
tokenizer.padding_side = "left"

base_model = AutoModel.from_pretrained("THUDM/chatglm2-6b", trust_remote_code=True)
if torch.cuda.is_available():
    base_model = base_model.half().cuda()
else:
    print("CUDA 不可用，模型将在 CPU 上加载和运行。")

lora_dir = "./lora_output"
if os.path.exists(lora_dir):
    print("加载已有的 LoRA 微调模型权重...")
    try:
        model = PeftModel.from_pretrained(base_model, lora_dir)
        if torch.cuda.is_available() and model.device.type == 'cpu':
          model = model.half().cuda()
        print("LoRA 微调模型加载完成。")
    except Exception as e:
        print(f"加载 LoRA 权重失败: {e}")
        print("尝试使用基础模型。")
        model = base_model
else:
    model = base_model
    print("未找到 LoRA 权重，使用基础模型。")

model.eval()

stu = []

TRAINING_DATA_FILE = "./train_data/sample.json"

initial_raw_train_data = [
    {
    "instruction": "你好，请自我介绍并说明你能提供什么帮助。",
    "input": "",
    "output": "您好！我是一个学生成绩管理系统，可以帮助您管理学生信息和成绩。我可以进行学生成绩的添加、编辑、删除、查询、排名以及图表展示等操作。如果您需要帮助，请告诉我具体的需求，例如“添加一个学生”或“查看所有学生的成绩”。"
    },
    {
    "instruction": "我想增加一个学生，名字叫小明。",
    "input": "",
    "output": "好的，要添加一个学生是吗？请提供学生小明的姓名和各科成绩，我会将他添加到系统中。"
    },
    {
        "instruction": "Describe the main idea of the text.",
        "input": "The capital of France is Paris, which is known for the Eiffel Tower.",
        "output": "AI transforms work and communication."
    },
    {
        "instruction": "Provide a definition for the following term.",
        "input": "Cloud computing allows users to access data and applications over the internet.",
        "output": "Mystery novels are popular due to their suspense."
    },
    {
        "instruction": "Rewrite the paragraph in a more formal tone.",
        "input": "She was running late and forgot her keys at home.",
        "output": "A fox jumps over a dog."
    },
    {
        "instruction": "Rewrite the paragraph in a more formal tone.",
        "input": "Photosynthesis is the process by which green plants make their own food.",
        "output": "Paris is the capital of France, famous for the Eiffel Tower."
    },
    {
        "instruction": "Explain the meaning of the sentence.",
        "input": "The quick brown fox jumps over the lazy dog.",
        "output": "He goes to school every day on foot."
    },
    {
        "instruction": "Generate a list of questions from the passage.",
        "input": "She was running late and forgot her keys at home.",
        "output": "Green plants produce food through photosynthesis."
    },
    {
        "instruction": "Summarize the following passage.",
        "input": "Once upon a time in a land far away, there lived a wise old owl.",
        "output": "She forgot her keys because she was late."
    },
    {
        "instruction": "Explain the meaning of the sentence.",
        "input": "Many people enjoy reading mystery novels because of their suspenseful plots.",
        "output": "There lived an owl in a distant land."
    },
    {
        "instruction": "Generate a list of questions from the passage.",
        "input": "The quick brown fox jumps over the lazy dog.",
        "output": "A fox jumps over a dog."
    }
]

for entry in initial_raw_train_data:
    if 'output' in entry and not isinstance(entry['output'], str):
        entry['output'] = str(entry['output'])


raw_train_data = []
if os.path.exists(TRAINING_DATA_FILE):
    with open(TRAINING_DATA_FILE, 'r', encoding='utf-8') as f:
        try:
            loaded_data = json.load(f)
            cleaned_data = []
            for entry in loaded_data:
                if isinstance(entry, dict) and 'output' in entry:
                    if not isinstance(entry['output'], str):
                        entry['output'] = str(entry['output'])
                    cleaned_data.append(entry)
                else:
                    print(f"发现无效训练数据条目，已跳过: {entry}")
            raw_train_data = cleaned_data
            print(f"从 {TRAINING_DATA_FILE} 加载了 {len(raw_train_data)} 条训练数据。")
        except json.JSONDecodeError:
            print(f"{TRAINING_DATA_FILE} 文件格式错误，将使用初始数据。")
            raw_train_data = initial_raw_train_data
else:
    print(f"{TRAINING_DATA_FILE} 文件不存在，将使用初始数据。")
    raw_train_data = initial_raw_train_data
    os.makedirs(os.path.dirname(TRAINING_DATA_FILE), exist_ok=True)
    with open(TRAINING_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(raw_train_data, f, ensure_ascii=False, indent=2)
    print(f"初始训练数据已保存到 {TRAINING_DATA_FILE}。")


class Student:
    def __init__(self,n,g):
        self.name = n
        self.gradesnum = g
        self.id = uuid.uuid4().hex[:8]
        self.gra = []
        self.subjects = []
           
    def askg(self):
        self.gra = []
        self.subjects = []
        for i in range(self.gradesnum):
            subject = input(f"Enter Subject Name # {i+1} For {self.name}: ")
            while True:
                try:
                    grade = float(input(f"Please Enter {self.name}'s Grade For {subject}: "))
                    if 0 <= grade <= 100:
                        self.subjects.append(subject)
                        self.gra.append(grade)
                        print(self.gra)
                        break
                    else:
                        print('!Grade Must Be Between 0 to 100!')
                except ValueError as ve:
                    print(f'!Please Enter a Valid Number: {ve}!')
                except Exception as e:
                    print(f'!Unexpected Error: {e}!')
        return self.gra, self.subjects

       
    def average(self):
        Grades = 0.00
        if self.gradesnum > 0:
            for i in range(0,self.gradesnum,1):
                Grades = Grades + self.gra[i]
            average = Grades/self.gradesnum
            return average
        else:
            return 0.0

       
    def highg(self):
        highg = 0
        if self.gradesnum > 0:
            for i in range(0,self.gradesnum,1):
                if(self.gra[i]>highg):
                    highg = self.gra[i]
            return highg
        else:
            return 0.0
       
    def lowg(self):
        lowg = 100
        if self.gradesnum > 0:
            for i in range(0,self.gradesnum,1):
                if(self.gra[i]<lowg):
                    lowg = self.gra[i]
            return lowg
        else:
            return 0.0
   
def quicksorthigh(students):
    if len(students) <= 1:
        return students
    pivot = students[0]
    pivota = pivot.average()
    left = []
    right = []
    for i in range(1,len(students),1):
        if students[i].average() > pivota:
            left.append(students[i])
        else:
            right.append(students[i])
    return quicksorthigh(left) + [pivot] + quicksorthigh(right)

def train_lora(single_step=False):
    global model
    print("正在使用新数据实时微调模型...")

    if not isinstance(model, PeftModel):
        print("将基础模型转换为 LoRA 微调模型...")
        peft_config = LoraConfig(
            task_type=TaskType.CAUSAL_LM,
            inference_mode=False,
            r=8,
            lora_alpha=32,
            lora_dropout=0.1,
            target_modules=["query_key_value"]
        )
        model = get_peft_model(model, peft_config)
        if torch.cuda.is_available() and model.device.type == 'cpu':
            model = model.cuda()
   
    model.train()
   
    global raw_train_data
    if os.path.exists(TRAINING_DATA_FILE):
        with open(TRAINING_DATA_FILE, 'r', encoding='utf-8') as f:
            try:
                loaded_data = json.load(f)
                cleaned_data = []
                for entry in loaded_data:
                    if isinstance(entry, dict) and 'output' in entry:
                        if not isinstance(entry['output'], str):
                            entry['output'] = str(entry['output'])
                        cleaned_data.append(entry)
                    else:
                        print(f"⚠️ 发现无效训练数据条目，已跳过 (train_lora): {entry}")
                raw_train_data = cleaned_data
            except json.JSONDecodeError:
                print(f"{TRAINING_DATA_FILE} 文件格式错误 (train_lora)，可能导致微调失败。")
                return
   
    if not raw_train_data:
        print("没有训练数据，跳过微调。")
        model.eval()
        return

    data = Dataset.from_list(raw_train_data)
   
    def tokenize_fn(example):
        prompt = example['instruction']
        if example.get('input', ''):
            prompt += '\n' + example['input']
        response = str(example.get('output', ''))
        text = f"[Round 1]\n问：{prompt}\n答：{response}"
        tokenized_output = tokenizer(text, truncation=True, max_length=512, padding="max_length")
        tokenized_output["labels"] = tokenized_output["input_ids"].copy()
        return tokenized_output

    tokenized_data = data.map(tokenize_fn, batched=False, remove_columns=data.column_names) # 【重要修改】 batched=False

    training_args = TrainingArguments(
        output_dir="./output",
        per_device_train_batch_size=1,
        gradient_accumulation_steps=1,
        num_train_epochs=1 if single_step else 3,
        logging_steps=10,
        save_steps=20,
        learning_rate=2e-4,
        fp16=True,
        save_total_limit=1,
        report_to="none",
        dataloader_num_workers=0,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_data,
    )

    print("开始训练...")
    try:
        trainer.train()
        print("训练完成")
        trainer.save_model(lora_dir)
        print("微调模型权重已保存。")
    except Exception as e:
        print(f"训练失败: {e}")
    model.eval()
    print("模型已切换到评估模式。")

def load_lora_model():
    global model
    print("加载微调后的模型 (此函数现在主要用于调试或手动刷新模型状态)...")
    if isinstance(model, PeftModel) and os.path.exists(lora_dir):
        print("模型已是 LoRA 微调模型，假设权重已是最新的。")
        return
   
    model_name = "THUDM/chatglm2-6b"
    current_base_model = AutoModel.from_pretrained(model_name, trust_remote_code=True)
    if torch.cuda.is_available():
        current_base_model = current_base_model.half().cuda()
   
    peft_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        inference_mode=True,
        r=8,
        lora_alpha=32,
        lora_dropout=0.1,
        target_modules=["query_key_value"]
    )
    model = get_peft_model(current_base_model, peft_config)
   
    if os.path.exists(lora_dir):
        model = PeftModel.from_pretrained(model, lora_dir)
        print("微调模型加载完成。")
    else:
        print("未找到 LoRA 权重，将使用基础模型。")
    model.eval()


def quicksortlow(students):
    if len(students) <= 1:
        return students
    pivot = students[0]
    pivota = pivot.average()
    left = []
    right = []
    for i in range(1,len(students),1):
        if students[i].average() < pivota:
            left.append(students[i])
        else:
            right.append(students[i])
    return quicksortlow(left) + [pivot] + quicksortlow(right)

def allgradeschart(students):
    print('All Students Grades Chart')
    for s in students:
        for subject, grade in zip(s.subjects, s.gra):
            bar = '█'* (int(grade)//2)
            print(f"{s.name:<6} - {subject:<10} | {bar} {grade}")
        print('-'* 30)

def ai_chat(prompt):
    global model
    if model.training:
        model.eval()

    response, _ = model.chat(tokenizer, prompt, history=[], max_new_tokens=512)
    print(f"AI Response: {response}")

    save_to_training_data(prompt, response)
   
    try:
        train_lora(single_step=True)
    except Exception as e:
        print(f"实时微调失败: {e}")
        model.eval()
    return response

def save_to_training_data(prompt, response):
    global raw_train_data
    global TRAINING_DATA_FILE

    sample = {
        "instruction": prompt,
        "input": "",
        "output": str(response)
    }
    raw_train_data.append(sample)

    os.makedirs(os.path.dirname(TRAINING_DATA_FILE), exist_ok=True)
    with open(TRAINING_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(raw_train_data, f, ensure_ascii=False, indent=2)
    print(f"新的交互已添加到内存并保存到 {TRAINING_DATA_FILE}。")

def test():
    s1 = Student('John',3)
    s1.subjects = ['Math','Social','English']
    s1.gra = [98,67,87]
   
    s2 = Student('Tony',3)
    s2.subjects = ['Math','Social','English']
    s2.gra = [77,88,99]
   
    s3 = Student('Ton',3)
    s3.subjects = ['Math','Social','English']
    s3.gra = [55,99,100]
   
    students = [s1,s2,s3]
   
    print('All Students Info')
    for s in students:
        print(s.name)
        print(f"Average: {s.average():.2f}")
        print(f"High Grade: {s.highg()}")
        print(f"Low Grade: {s.lowg()}")
       
    print('Ranking High to Low')
    ranking = quicksorthigh(students)
    for i, s in enumerate(ranking, 1):
        print(f"{i}. {s.name} - Average: {s.average():.2f}")
       
    print('Ranking Low to High')
    ranking = quicksortlow(students)
    for i, s in enumerate(ranking, 1):
        print(f"{i}. {s.name} - Average: {s.average():.2f}")
       
    print('All Grades Chart')
    allgradeschart(students)

    print('AI Chat Test')
    prompt = "I am testing the feature,if you can get it please introduce yourself and reply that you are ready to assist. "
    response = ai_chat(prompt)

print("Do You Want to Run Test First? (y/n)")
asktest = input('>>>')
try:
    if asktest == 'y':
        test()
        print('')
        print('Test Completed')
        print('-'* 100)
        print('Enter The Program')
        print('')
    else:
        print('No Test, Enter The Program')
except Exception as e:
    print('')
    print('!Program Error!')
    print('Error Message:',e)
    print('')

while True:    
    try:
        namenum = int(input('How Many Student? '))
        break
    except Exception as e:
        print('')
        print('!Please Enter Number!')
        print('Error Message:',e)
        print('')

for i in range(namenum):
    while True:
        try:
            print('')
            name = input('Please Enter Name: ')
            s = Student(name, 0)
            print(f"\n{s.name}'s ID: {s.id}\n")

            gradenum = int(input('How Many Grades? '))
            s.gradesnum = gradenum
            s.gra, s.subjects = s.askg()
            stu.append(s)
            break
        except ValueError:
            print('')
            print('!Please Enter Number!')
            print('')
        except Exception as e:
            print(f'!Unexpected Error: {e}!')

def handle_ranking():
    if not stu:
        print("There is currently no student data, please add it first.")
        return
    ranking = str(input('Do You Want High To Low Ranking(hl) or Low To High Ranking(lh)'))
    if(ranking == 'hl'):
        ranking = quicksorthigh(stu)
        print('Student Ranking by Average Score High to Low')
        for i, s in enumerate(ranking, 1):
            print(f"{i}. {s.name} Average: {s.average():.2f}")
    elif(ranking == 'lh'):
        ranking = quicksortlow(stu)
        print('Student Ranking by Average Score Low to High')
        for i, s in enumerate(ranking, 1):
                print(f"{i}. {s.name} Average: {s.average():.2f}")
    else:
        print()
        print('!Invalid Input for Ranking (should be "hl" or "lh")!')
        print()

def ai_analysis():
    print("Please enter your request in natural language (e.g., add a student, view grades, modify grades, save, etc.):")
    prompt = input('>>> ')
    if not prompt.strip():
        print("!No input provided! Please enter a valid command.")
        return
    result = ai_chat(prompt)
    result = result.lower()
    print("AI Analysis Result:")
    print(result)

    if "add" in result and "student" in result:
        add()
    elif "save" in result:
        save()
    elif "edit" in result or "modify" in result:
        edit()
    elif "show" in result or "view" in result:
        allgradeschart(stu)
    elif "rank" in result or "ranking" in result:
        handle_ranking()
    else:
        print("!Unable to recognize the command at the moment! Please try rephrasing.")

def save():
    if not stu:
        print("There is currently no student data, please add it first.")
        return
    save = input('Do You Want To Save The Data To a File? (y/n): ')
    try:
        if save.lower() == 'y':
            with open('students.txt','w',encoding = 'utf-8')as f:
                for s in stu:
                    f.write(f"name: {s.name} (ID: {s.id})\n")
                    for sub, gra in zip(s.subjects, s.gra):
                        f.write(f" {sub}: {gra}\n")
                    f.write("\n")
                print('Data Saved To students.txt')
        elif save.lower() == 'n':
            print('Data Not Save')
        else:
            print()
            print('!Invalid Input for Save (should be "y" or "n")!')
            print()
    except IOError as e:
        print('')
        print(f"Failed To Save Data: {e}")
        print('')
    except Exception as e:
        print(f'!Unexpected Error: {e}!')

def add():
    print('Please Enter Name')
    name = input('>>>')
    s = Student(name,0)
    while True:
        try:
            print('How Many Grades?')
            gradenum = int(input('>>>'))
            s.gradesnum = gradenum
            break
        except ValueError:
            print('!Please Enter Number!')
        except Exception as e:
            print(f'!Unexpected Error: {e}!')
    s.gra, s.subjects = s.askg()
    stu.append(s)
    print(f"Student {s.name} Added Successfully")
    print(f"ID: {s.id}")

def edit():
    if not stu:
        print("There is currently no student data, please add it first.")
        return
    print('Which Student Do You Want To Edit? (Name or ID)')    
    ename = input('>>>')
    found = False
    for s in stu:
        if s.name == ename or s.id == ename:
            print(s.name+"'s Grades")
            for i, grade in enumerate(s.gra):
                print(f"{i+1}. {s.subjects[i]}: {grade}")
            try:
                index = int(input('Enter The Grade Number You Want To Change: ')) - 1
                if 0 <= index < len(s.gra):
                    newgrade = float(input('Enter New Grade: '))
                    if 0 <= newgrade <= 100:
                        s.gra[index] = newgrade
                        print('Grade Update successfully')
                        print(f"Updated Grades For {s.name}:")
                        for i, grade in enumerate(s.gra):
                            print(f"{s.subjects[i]}: {grade}")
                    else:
                        print('')
                        print('!Invalid Grade! Must Be Between 0 to 100!')
                        print('')
                else:
                    print('')
                    print("!Invalid Grade Number!")
                    print('')
            except ValueError as ve:
                print('')
                print('!Please Enter Number!', ve)
                print('')
            except Exception as e:
                print(f'!Unexpected Error: {e}!')
            found = True
            break
    if not found:
        print('')
        print(f"!Student Name {ename} Not Found! Please Check The Name And Try Again")
        print('')

def delete():
    if not stu:
        print("There is currently no student data, please add it first.")
        return      
    dname = []
    print( 'Which Student Do Your Want To Delete?')
    dname = input('>>>')
    deleted = False
    for s in stu:
        if(dname == s.name):
            stu.remove(s)
            print(dname,'Deleted')
            deleted = True
            break
    if not deleted:
        print('')
        print(dname,'Not Found')
        print('')

def all_grade():
    if not stu:
        print("There is currently no student data, please add it first.")
        return
    for s in stu:
        print('Name:',s.name)
        print('ID:',s.id)
        print('All Grades', list(zip(s.subjects, s.gra)))
        for i,grade in enumerate(s.gra):
            print(f"{s.subjects[i]}:{grade}")
        print('-'* 30)
    allgradeschart(stu)

def found():
    if not stu:
        print("There is currently no student data, please add it first.")
        return
    not_found = True
    print('Enter the name or ID of the student you want to check:')
    sname = input('>>>')
    for s in stu:
        if (s.name == sname or sname == s.id):
            print('Name:',s.name)
            print('ID:',s.id)
            print('All Grades', list(zip(s.subjects, s.gra)))
            for i,grade in enumerate(s.gra):
                print(f"{s.subjects[i]}:{grade}")
            print(f"Average = {s.average():.2f}")
            print('Highgrade = ',s.highg())
            print('Lowgrade = ',s.lowg())
            not_found = False
            break
    if not_found:
        print('')
        print('!No Found!')
        print('')


while True:    
    print('Options: AI|Save Data|Edit|Add|Delete|Ranking|Found|All Grade|Test|Exit')
    an = input('>>>')
    choice = an.replace(" ", "").lower()
    if choice == 'ranking':
        handle_ranking()
        continue
   
    elif choice in ['save data','save']:
        save()
        continue
   
    elif choice == 'add':
        add()
        continue
   
    elif choice == 'edit':
        edit()
        continue      
       
    elif choice == 'delete':
        delete()
        continue
   
    elif choice == 'all grade':
        all_grade()
        continue
   
    elif choice == 'test':
        test()
        continue
   
    elif choice == 'found':
        found()
        continue

    elif choice == 'exit':
        print('')
        print('Exiting Program')
        print('')
        break

    elif choice == 'ai':
        ai_analysis()
        continue
   
    else:
        print('')
        print('!Invalid Option! Please Choose Save Data, Edit, Add, Ranking, Found, All Grade, Test, or Exit')
        print('')
        continue