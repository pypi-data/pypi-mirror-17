#!/usr/bin/env python

import os, sys, glob, yaml, zipfile

# Append yaml dependences in yaml_file ('import' files) to another yaml file (full_yaml_file)
def addDependencies(file_list, filename):
    # print 'Checking for dependencies on:', os.path.normpath(filename)
    file_list.append(os.path.normpath(filename))
    folder = os.path.dirname(filename)
    yaml_file = yaml.safe_load(open(filename))

    # Search for fonts or textures urls
    if 'fonts' in yaml_file:
        for font in yaml_file['fonts']:
            if 'url' in yaml_file['fonts'][font]:
                file_list.append(os.path.normpath(folder + '/' + yaml_file['fonts'][font]['url']))

    if 'textures' in yaml_file:
        for font in yaml_file['textures']:
            if 'url' in yaml_file['textures'][font]:
                file_list.append(os.path.normpath(folder + '/' + yaml_file['textures'][font]['url']))

    # Search for inner dependemcies
    if 'import' in yaml_file:
        if (type(yaml_file['import']) is str):
            addDependencies(file_list, folder + '/' + yaml_file['import'])
        else:
            for file in yaml_file['import']:
                addDependencies(file_list, folder + '/' + file)

def zip(files, dst):
    zf = zipfile.ZipFile("%s.zip" % (dst), "w", zipfile.ZIP_DEFLATED)
    abs_src = os.path.abspath(src)
    for dirname, subdirs, files in os.walk(src):
        for filename in files:
            absname = os.path.abspath(os.path.join(dirname, filename))
            arcname = absname[len(abs_src) + 1:]
            print 'zipping %s as %s' % (os.path.join(dirname, filename),
                                        arcname)
            zf.write(absname, arcname)
    zf.close()

# ================================== Main functions
def bundler(full_filename):
    print full_filename, os.getcwd()
    filename, file_extension = os.path.splitext(full_filename)
    if file_extension == '.yaml':
        all_dependencies = [] 
        addDependencies(all_dependencies, './'+full_filename)
        files = list(set(all_dependencies))

        print "Bundling ",filename,"width",len(files),"dependencies, into ",filename+".zip"
        zipf = zipfile.ZipFile(filename+'.zip', 'w', zipfile.ZIP_DEFLATED)
        for file in files:
            zipf.write(file)
        zipf.close()
    else:
        print 'Error: file', 

def main():
    if len(sys.argv) > 1:
        bundler(sys.argv[1])
    else:
        bundler(raw_input("What Tangram YAML scene file do you want to bundle into a zipfile?: "))
    
if __name__ == "__main__":
    exit(main())
