
import detect
import traverse

count = 0

output_file = open('output_file.txt', "a")
         
def run(path):
    global count
    file = str(path)
    count += 1
    output_file.write(file + "\n")
    detect.detect_face(file, f"img{count}")

    if count % 10 == 0:
        print(count)
        output_file.flush()

if __name__ == '__main__':
    traverse.traverse_files("K:\Documents\Jenya", run)
    output_file.close()
