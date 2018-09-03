
import os
import sys
import codecs
import stat
import shutil
from codecs import BOM_UTF8

def makeMutable(fileNameOrDirName): 
	if (not os.path.exists(fileNameOrDirName)): 
		return
	if (os.path.isfile(fileNameOrDirName)): 
		os.chmod(fileNameOrDirName, stat.S_IWUSR | stat.S_IRUSR)
		return
	for file in os.listdir(fileNameOrDirName): 
		subFile = os.path.join(fileNameOrDirName, file) 
		makeMutable(subFile)

def delete(fileNameOrDirName): 
	if (not os.path.exists(fileNameOrDirName)): 
		return
	makeMutable(fileNameOrDirName)
	if os.path.isfile(fileNameOrDirName): 
		os.remove(fileNameOrDirName)
		return
	else: 
		shutil.rmtree(fileNameOrDirName)
		return

def getFiles(dirName, suffix):
	currentDir = os.path.abspath(os.path.dirname(__file__))
	dirName = os.path.join(currentDir, dirName)
	dirName = os.path.abspath(dirName)
	dirs = [dirName]
	files = []
	while (len(dirs) > 0):
		thisDirName = dirs.pop()
		try: 
			fileList = os.listdir(thisDirName)
		except Exception as e:
			return []

		for file in fileList:
			filepath = os.path.join(thisDirName, file)
			if (os.path.isdir(filepath)):
				subFiles = getFiles(filepath, suffix)
				for subFile in subFiles:
					files.append(subFile)
				continue

		for file in fileList:
			filepath = os.path.join(thisDirName, file)
			if (os.path.isdir(filepath)):
				continue
			fileSuffix = os.path.splitext(filepath)[1]
			fileSuffix = fileSuffix.lower()
			if (fileSuffix != suffix):
				continue
			files.append(filepath)
	return files

def __lstrip_bom(str_, bom=BOM_UTF8):
	if str_.startswith(bom):
		return str_[len(bom):]
	else:
		return str_

def readFileText(filename):
	file_object = None
	content = ""
	try: 
		file_object = open(filename, "rb")
		content = file_object.read()
		content = __lstrip_bom(content)
		content = content.decode("utf-8")
	except Exception as e:
		return content
	finally: 
		if (not file_object is None): 
			file_object.close()
	return content

def writeFileText(filename, text):
	file_object = None
	try:
		file_object = open(filename, 'wb')
		bytes = text.encode("utf-8-sig")
		file_object.write(bytes)
		file_object.close()
	except Exception as e:
		print (e)
		return
	finally:
		if (not file_object is None):
			file_object.close()

def mergeFilesExcept(path, suffix, exceptFileBaseNames):
	files = getFiles(path, suffix)
	allTexts = ""
	i = 0
	while (i < len(exceptFileBaseNames)):
		exceptFileBaseNames[i] = exceptFileBaseNames[i].lower()
		i += 1
	for f in files:
		baseNameLower = os.path.basename(f).lower()
		isExceptFile = False
		for candiateBaseName in exceptFileBaseNames:
			if (candiateBaseName == baseNameLower):
				isExceptFile = True
				break
		if (isExceptFile):
			continue

		text = readFileText(f)
		allTexts = allTexts + text + "\r\n"
	return allTexts

def safeMakeDirs(dirs): 
	if (os.path.isfile(dirs)): 
		return
	if not os.path.exists(dirs):  
		os.makedirs(dirs)

def postBuild():
	currentDir = os.path.abspath(os.path.dirname(__file__))
	currentDir = os.path.abspath(os.path.join(currentDir, "../obj_ts"))
	allTexts = ""
	allTexts += readFileText(os.path.join(currentDir, "easyar_runtime.js"))
	allTexts += "\r\n"
	allTexts += mergeFilesExcept(currentDir, ".js", ["easyar_runtime.js", "Program.js", "Environment.js"])
	allTexts += "\r\n"
	allTexts += readFileText(os.path.join(currentDir, "Environment.js"))
	allTexts += "\r\n"
	allTexts += readFileText(os.path.join(currentDir, "Program.js"))
	allTexts += "\r\n"

	outputDir = os.path.join(currentDir, "../assets")
	safeMakeDirs(outputDir)

	appJsName = os.path.join(outputDir, "app.js")
	appJsName = os.path.abspath(appJsName)
	delete(appJsName)
	writeFileText(appJsName, allTexts)
	print("Code is generated at " + appJsName)

	allTexts = ""
	allTexts += mergeFilesExcept(currentDir, ".ts", ["easyar_runtime.d.ts"])
	appTsName = os.path.join(outputDir, "app.ts")
	appTsName = os.path.abspath(appTsName)
	delete(appTsName)
	writeFileText(appTsName, allTexts)
	print("Declaration Code is generated at " + appTsName)

postBuild()
