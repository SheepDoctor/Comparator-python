import os
import subprocess
import time

class Java():
    def compile_java(path, name):
        subprocess.check_call(['javac', os.path.join(path, name + '.java')])
        
    def run_java(path, name, test_path):
        cmd = ['java', os.path.join(path, name).replace("\\", "/")]
        with open(os.path.join(path, name + '.out'), 'w') as file:
            with open(test_path, 'r') as f: 
                t = time.time()
                result = subprocess.run(cmd, stdin=f, stdout=file, stderr=subprocess.PIPE, text=True)     
                t = time.time() - t
        return t
        
    def run(path, name, compile, test_path='./test.in'):
        if compile:
            Java.compile_java(path, name)       
        t = Java.run_java(path, name, test_path)     
        return t, os.path.join(path, name + '.out') 

class Cpp():
    def compile_cpp(path, name):
        subprocess.check_call(['g++', os.path.join(path, name + '.cpp'), '-o', os.path.join(path, name)])
        
    def run_cpp(path, name, test_path):
        cmd = [os.path.join(path,name)]
        with open(os.path.join(path, name + '.out'), 'w') as file:
            with open(test_path, 'r') as f:
                t = time.time()
                result = subprocess.run(cmd, stdin=f, stdout=file, stderr=subprocess.PIPE, text=True)     
                t = time.time() - t
        return t, os.path.join(path, name + '.out') 
    
    def run(path, name, compile, test_path='./test.in'):
        if compile:
            Cpp.compile_cpp(path, name)  
        t = Cpp.run_cpp(path, name, test_path)     
        return t

class Python():
    def run(path, name, compile, test_path='./test.in'):
        cmd = ['python', os.path.join(path, name + '.py')]
        with open(os.path.join(path, name + '.out'), 'w') as file:
            with open(test_path, 'r') as f:
                t = time.time()
                result = subprocess.run(cmd, stdin=f, stdout=file, stderr=subprocess.PIPE, text=True)
                t = time.time() - t
        return t, os.path.join(path, name + '.out') 

def calculate(size, compile=False, path1='Java/test.java', path2='Python/test.py'):
    cmd = ['python', './test_case.py'] + [str(x) for x in size]
    test_path = './test.in'
    with open(test_path, 'w') as file:
        result = subprocess.run(cmd, stdout=file, stderr=subprocess.PIPE, text=True)
    
    path = os.path.basename(path1)
    if path1[-3:] == 'cpp':
        t1, out1 = Cpp.run(os.path.dirname(path1), os.path.basename(path1)[:-4], compile, test_path)
    elif path1[-4:] == 'java':
        t1, out1 = Java.run(os.path.dirname(path1), os.path.basename(path1)[:-5], compile, test_path)
    elif path1[-2:] == 'py':
        t1, out1 = Python.run(os.path.dirname(path1), os.path.basename(path1)[:-3], compile, test_path)
    
    if path2[-4:] == 'java':
        t2, out2 = Java.run(os.path.dirname(path2), os.path.basename(path2)[:-5], compile, test_path)
    elif path2[-3:] == 'cpp':
        t2, out2 = Cpp.run(os.path.dirname(path2), os.path.basename(path2)[:-4], compile, test_path)
    elif path2[-2:] == 'py':
        t2, out2 = Python.run(os.path.dirname(path2), os.path.basename(path2)[:-3], compile, test_path)
    return t1, t2, out1, out2

def compare_files(file1, file2):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        f1_lines = (line.rstrip() for line in f1)
        f2_lines = (line.rstrip() for line in f2)

        for line1, line2 in zip(f1_lines, f2_lines):
            if line1 != line2:
                return False
        return next(f1_lines, None) == next(f2_lines, None)

def compare(t1, t2, out1, out2, iter):
    #TODO：这里按照自定义方式检查时间
    # if t2 > 1:
    #     print("Iteration {}: Time exceeded!".format(iter))
    if compare_files(out1, out2):
        print("Iteration {}: Answer accepted.".format(iter))
    else:
        print("Iteration {}: Wrong answer!".format(iter))
    
    
def main(size, path1, path2, iter):
    compile=False
    if iter == 1:
        compile = True
    if path1 != "" and path2 == "": 
        t1, t2, out1, out2=calculate(size, compile, path1)
    elif path2 != "" and path1 == "":
        t1, t2, out1, out2=calculate(size, compile, path2)
    elif path1 != "" and path2 != "":
        t1, t2, out1, out2=calculate(size, compile, path1, path2)
    else:
        t1, t2, out1, out2=calculate(size, compile)
    
    compare(t1, t2, out1, out2, iter)

if __name__ == '__main__':
    iter = 100
    size = ['10']
    path1 = "Java/test.java"
    path2 = "Cpp/test.py"
    for i in range(iter):
        main(size, path1, path2, i)