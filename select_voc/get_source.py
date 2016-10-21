#/***************************************************************************
# *
# * Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
# *
# **************************************************************************/
#
#
#
#/**
# * @file get_source.py
# * @author quanzongfeng(com@baidu.com)
# * @date 2014/11/18 11:23:11
# * @brief
# *
# **/
#
import os
import sys
import ConfigParser
import buildgraph
import graphscript
import voc2dict
import modelscript
import cmd
import msg
import modelenv
import sourceenv
import getopt

DEFAULT_CHECK_SCRIPT = "create_script/check.sh"
DEFAULT_BUILD_SCRIPT_DIR = 'buildgraph'
DEFAULT_MODEL_DIR = 'model'
DEFAULT_SOURCE_DIR = 'source'
DEFAULT_VOC2DICT_DIR = 'voc2dict'
DEFAULT_GRAPH_SCRIPT_DIR = 'graphscript'
DEFAULT_MODEL_SCRIPT_DIR = 'modelscript'
DEFAULT_TYPE = 'buildgraph'


class TargetConf:
    def __init__(self, confFile):
        self.Path = os.getcwd() + os.sep

        cf = ConfigParser.ConfigParser()
        cf.read(confFile)
        self.config = cf
        self.state = 0
        self.continous = False
        self.confFile = confFile

        try:
            self.type = cf.get('global', 'type')
        except:
            self.type = DEFAULT_TYPE

        try:
            self.targetName = cf.get('global', 'name')
        except:
            msg.raise_cmd('no target name in %s' % confFile)

        try:
            self.targetDir = cf.get('global', 'target_path')
        except:
            self.targetDir = os.getcwd()

        if self.targetDir == "":
            self.targetDir = os.getcwd()
        if self.targetDir[0] != os.sep:
            self.targetDir = self.Path + self.targetDir
        if self.targetDir[-1] != os.sep:
            self.targetDir += os.sep

        if os.path.isdir(self.targetDir) == False:
            os.makedirs(self.targetDir)

        try:
            self.checkScript = cf.get('global', 'check_full_script')
        except:
            self.checkScript = DEFAULT_CHECK_SCRIPT

        try:
            self.state = cf.getint('global', 'state')
            self.continous = cf.getbool('global', 'continous')
        except:
            pass

#        try:
#            self.buildGraphScriptDir = cf.get('global', 'graph_script_dir')
#        except:
#            self.buildGraphScriptDir = DEFAULT_BUILD_SCRIPT_DIR

        self.modelDir = DEFAULT_MODEL_DIR
        self.sourceDir = DEFAULT_SOURCE_DIR

        try:
            self.modelDir = cf.get('global', 'model_dir')
            self.sourceDir = cf.get('global', 'source_dir')
        except:
            pass
        if self.modelDir[0] != os.sep:
            self.modelDir = self.targetDir + self.modelDir
        if self.sourceDir[0] != os.sep:
            self.sourceDir = self.targetDir + self.sourceDir

        if os.path.isdir(self.sourceDir) == False:
            os.makedirs(self.sourceDir)
        if os.path.isdir(self.modelDir) == False:
            os.makedirs(self.modelDir)

        try:
            self.host = cf.get('global', 'host')
            self.path = cf.get('global', 'path')
        except:
            self.host = ''
            self.path = ''

        self.reBuildLmla = False
        self.reBuildGraph = False
        self.reBuildFsn = False
        self.reBuildLm = False

        try:
            self.reBuildLmla = cf.get('global', 'rebuild_lmla')
        except:
            pass

        try:
            self.reBuildGraph = cf.get('gblaol', 'rebuild_graph')
        except:
            pass

        try:
            self.reBuildFsn = cf.get('global', 'rebuild_fsn')
        except:
            pass

        try:
            self.reBuildLm = cf.get('global', 'rebuild_lm')
        except:
            pass

        self.graphList = ""
        self.graphScript = ''
        self.modelList = ""
        self.voc2dict = ""
        self.sourceList = ""
        self.modelScript = ""
        self.rebuildModelList = []
        self.addCaidanModels = {}

    def processRebuildModelList(self):
        """get rebuild model list and caidan models """
        cf = self.config
        if 'rebuild_model_list' in cf.sections():
            for k, v in cf.items('rebuild_model_list'):
                self.rebuildModelList.append(v)

        if 'add_caidan_model_list' in cf.sections():
            for k, v in cf.items("add_caidan_model_list"):
                if v not in cf.sections():
                    msg.raise_cmd("%s configed caidan but not config [%s]" % (v, v))
                target = cf.get(v, 'target')
                self.addCaidanModels.setdefault(target, {})
                coef = cf.get(v, 'mix_coef')
                self.addCaidanModels[target]['mix_coef'] = coef

                for n, val in cf.items(v):
                    if n.startswith('source'):
                        self.addCaidanModels[target].setdefault(val, {})
                for source in self.addCaidanModels[target].keys():
                    if source != 'mix_coef':
                        if source not in cf.sections():
                            msg.war("source %s in caidan but not configed host \
                                        and path; Use default" % source)
                            continue
                 #          msg.raise_cmd("found not configed source %s" % source)
                        host = cf.get(source, 'host')
                        path = cf.get(source, 'path')
                        self.addCaidanModels[target][source]['host'] = host
                        self.addCaidanModels[target][source]['path'] = path
        elif 'add_caidan' in cf.sections():
            v = 'add_caidan'
            target = cf.get(v, 'target')
            self.addCaidanModels.setdefault(target, {})
            coef = cf.get(v, 'mix_coef')
            self.addCaidanModels[target]['mix_coef'] = coef

            for n, val in cf.sections():
                if n.startswith('source'):
                    self.addCaidanModels[target].setdefault(val, {})
            for source in self.addCaidanModels[target].keys():
                if source != 'mix_coef':
                    if source not in cf.sections():
                        msg.err("source %s in caidan but not configed host and path" % source)
                        msg.raise_cmd("found not configed source %s" % source)
                    host = cf.get(source, 'host')
                    path = cf.get(source, 'path')
                    self.addCaidanModels[target][source]['host'] = host
                    self.addCaidanModels[target][source]['path'] = path

        self.printCaidanModels()
        self.processCaidanSources()

    def processCaidanSources(self):
        """add caidan source host and path to sourcelist"""
        dt = self.addCaidanModels
        cf = ConfigParser.ConfigParser()
        cf.read(self.Path + self.sourceList)
        for k, aaa in dt.items():
            for t, val in dt[k].items():
                if t.startswith('source'):
                    if 'host' in val.keys():
                        host = val['host']
                        path = val['path']
                        source_name = t

                        if source_name in cf.sections():
                            msg.war("%s already in source_list, remove it first" % source_name)
                            cf.remove_section(source_name)
                        cf.add_section(source_name)
                        cf.set(source_name, 'host', host)
                        cf.set(source_name, 'path', path)
        cf.write(self.Path + self.sourceList)

    def printCaidanModels(self):
        """print caidan models"""
        for k, v in self.addCaidanModels.items():
            print "%s:" % k
            print "\tmix_coef: %s" % v['mix_coef']
            print "\tSources: "
            for so, val in v.items():
                if so == 'mix_coef':
                    continue
                if val != {}:
                    print "\t%s: %s:%s" % (so, val['host'], val['path'])
                else:
                    print "\t%s" % so
            print ""

    def checkDefaultSources(self):
        """check whether resources download or not"""
        if os.path.isfile(self.targetDir + 'graph_list.txt'):
            self.graphList = 'graph_list.txt'
        if os.path.isdir(self.targetDir + DEFAULT_GRAPH_SCRIPT_DIR):
            self.graphScript = DEFAULT_GRAPH_SCRIPT_DIR
        if os.path.isdir(self.targetDir + DEFAULT_MODEL_SCRIPT_DIR):
            self.modelScript = DEFAULT_MODEL_SCRIPT_DIR
        if os.path.isdir(self.targetDir + DEFAULT_VOC2DICT_DIR):
            self.voc2dict = DEFAULT_VOC2DICT_DIR
        if os.path.isfile(self.targetDir + 'source_list.txt'):
            self.sourceList = 'source_list.txt'
        if os.path.isfile(self.targetDir + 'model_list.txt'):
            self.modelList = 'model_list.txt'

    def downloadSources(self):
        """download model script/list, graph script/list, source list, voc2dict"""
        cf = self.config
        os.chdir(self.targetDir)

        if 'graph_list' in cf.sections():
            try:
                graph_path = cf.get('graph_list', 'path')
                graph_host = cf.get('graph_list', 'host')
            except:
                msg.raise_cmd("cat't get path and host in [graph_list]")

            re, lastcmd = cmd.wget_file(graph_host, graph_path, "graph_list.txt")
            if re[0] != 0:
                msg.raise_cmd("last syscmd wget Failed! ")
            self.graphList = "graph_list.txt"
        elif self.type == 'buildgraph' and self.host == '':
            msg.raise_cmd("[graph_list] host or path not configed")

        if 'graph_script' in cf.sections():
            try:
                buildgraph_host = cf.get('graph_script', 'host')
                buildgraph_path = cf.get('graph_script', 'path')
            except:
                msg.raise_cmd("cat not get host and path in [graph_script]")

            destGraph = DEFAULT_GRAPH_SCRIPT_DIR + os.sep
            if os.path.isdir(destGraph) == True:
                re, lastcmd = cmd.rm_dir(destGraph)
                if re[0] != 0:
                    msg.raise_cmd("last syscmd rm failed")
            os.makedirs(destGraph)

            re, lastcmd = cmd.wget_dir(buildgraph_host, buildgraph_path, destGraph, 0)
            if re[0] != 0:
                msg.raise_cmd("last syscmd failed")
            if self.checkGraphScript(destGraph) == False:
                msg.raise_cmd("check graph script failed")
            self.graphScript = destGraph

        elif self.type == 'buildgraph':
            msg.raise_cmd("[graph_script] path or host not configed ")

        if 'model_list' in cf.sections():
            try:
                model_path = cf.get('model_list', 'path')
                model_host = cf.get('model_list', 'host')
            except:
                msg.raise_cmd("[model_list] path or host not configed ")

            re, lastcmd = cmd.wget_file(model_host, model_path, "model_list.txt")
            if re[0] != 0:
                msg.raise_cmd("last syscmd wget Failed! ")
            self.modelList = "model_list.txt"
        else:
            msg.raise_cmd("[model_list] not configed")

        try:
            source_path = cf.get('source_list', 'path')
            source_host = cf.get('source_list', 'host')
        except:
            msg.raise_cmd("[source_list] path or host not configed ")

        re, lastcmd = cmd.wget_file(source_host, source_path, "source_list.txt")
        if re[0] != 0:
            msg.raise_cmd("last syscmd wget Failed! ")
        self.sourceList = "source_list.txt"

        try:
            voc2dict_host = cf.get('voc2dict', 'host')
            voc2dict_path = cf.get('voc2dict', 'path')
        except:
            msg.raise_cmd("[voc2dict] path or host not configed ")

        destVoc = DEFAULT_VOC2DICT_DIR + os.sep
        if os.path.isdir(destVoc) == False:
            os.makedirs(destVoc)
        re, lastcmd = cmd.wget_dir(voc2dict_host, voc2dict_path, destVoc, 0)
        if re[0] != 0:
            msg.raise_cmd("last syscmd failed")
        if self.checkVoc2Dict(destVoc) == False:
            msg.raise_cmd("check voc2dict failed")
        self.voc2dict = destVoc

        destModelGraph = DEFAULT_MODEL_SCRIPT_DIR + os.sep
        if os.path.isdir(destModelGraph) == True:
            re, lastcmd = cmd.rm_dir(destModelGraph)
            if re[0] != 0:
                msg.raise_cmd("last syscmd rm failed")
        os.makedirs(destModelGraph)

        try:
            model_script_host = cf.get('model_script', 'host')
            model_script_path = cf.get('model_script', 'path')
        except:
            msg.raise_cmd("[model_script] host or path not configed")
        re, lastcmd = cmd.wget_dir(model_script_host, model_script_path, destModelGraph, 0)
        if re[0] != 0:
            msg.raise_cmd("last syscmd failed")
        if self.checkModelScript(destModelGraph) == False:
            msg.raise_cmd("check model script:%s failed" % destModelGraph)
        self.modelScript = destModelGraph

        os.chdir(self.Path)

    def checkModelScript(self, destModelGraph):
        if 'ReadMe.txt' not in os.listdir(destModelGraph):
            return False
        ms = modelscript.ModelScript(destModelGraph + os.sep + 'ReadMe.txt', destModelGraph)
        ms.setCheckScript(self.Path + self.checkScript)
        return ms.checkFull()

    def checkVoc2Dict(self, destVoc):
        if 'ReadMe.txt' not in os.listdir(destVoc):
            return False
        voc = voc2dict.Voc2Dict(destVoc + os.sep + 'ReadMe.txt', destVoc)
        voc.buildVoc2Dict()
        return True

    def checkGraphScript(self, destGraph):
        if 'ReadMe.txt' not in os.listdir(destGraph):
            return False
        graph_script = graphscript.GraphScript(destGraph + os.sep + 'ReadMe.txt', destGraph)
        graph_script.setCheckScript(self.Path + self.checkScript)
        return graph_script.checkFull()

    def printconf(self):
        print "--------------------config start----------------"
        print 'Target Type: ' + self.type
        print 'Target Dir: ' + self.targetDir
        print 'Traget name: ' + self.targetName
        print 'Graph List: ' + self.graphList
        print 'Model List: ' + self.modelList
        print 'Voc2dict: ' + self.voc2dict
        print 'Build Script: ' + self.graphScript
        print 'Model Script: ' + self.modelScript
        print 'Model Download Dir :' + self.modelDir
        print 'Source Download Dir : ' + self.sourceDir
        print "--------------------config end------------------"

    def getGraph(self):
#first, check exist or not
        dn = os.listdir(self.targetDir)
        if self.targetName in dn:
            if self.checkGraphEnv(self.targetDir + '/' + self.targetName) == True:
                msg.log("checkGraphEnv already exist %s succeed" % (self.targetName))
                return
            else:
                msg.log("%s: exist but not fulled " % (self.targetDir + os.sep + self.targetName))
                re, lastcmd = cmd.rm_dir(self.targetDir + os.sep + self.targetName)
                if re[0] != 0:
                    msg.log("%s failed" % lastcmd)
                    msg.raise_cmd("%s failed" % lastcmd)

#if set in host and path in global section, just download it
        if self.type == 'buildgraph' and self.path != '' and self.host != '':
            re, lastcmd = wget_dir(self.host, self.path, self.targetDir + os.sep + self.targetName)
            if re[0] != 0:
                msg.raise_cmd('%s failed' % lastcmd)
            return

#else, download in self.graphList
        cf = ConfigParser.ConfigParser()
        cf.read(self.targetDir + os.sep + self.graphList)
        try:
            host = cf.get(self.targetName, 'host')
            path = cf.get(self.targetName, 'path')
        except:
            msg.raise_cmd("can't find host and path in %s for %s" % (self.graphList, self.targetName))
        msg.log("get host:%s and path:%s" % (host, path))

        re, lastcmd = cmd.wget_dir(host, path, self.targetDir + os.sep + self.targetName)
        if re[0] != 0:
            msg.raise_cmd("%s Failed!" % lastcmd)
        return

    def getModel(self):
        dn = os.listdir(self.targetDir)
        if self.targetName in dn:
            if self.checkModelEnv(self.targetDir + '/' + self.targetName) == True:
                msg.log("modelenv:%s  already exist" % self.targetName)
                return
            else:
                re, lastcmd = cmd.rm_dir(self.targetDir + os.sep + self.targetName)
                if re[0] != 0:
                    msg.raise_cmd("%s failed" % lastcmd)

        if self.type == 'model' and self.path != '' and self.host != '':
            re, lastcmd = cmd.wget_dir(self.host, self.path, self.targetDir + os.sep + self.targetName)
            if re[0] != 0:
                msg.raise_cmd("%s failed" % lastcmd)
            return

        cf = ConfigParser.ConfigParser()
        cf.read(self.targetDir + os.sep + self.modelList)
        try:
            host = cf.get(self.targetName, 'host')
            path = cf.get(self.targetName, 'path')
        except:
            msg.raise_cmd("get host/path in %s for %s failed" % (self.modelList, self.targetName))

        re, lastcmd = cmd.wget_dir(host, path, self.targetDir + os.sep + self.targetName)
        if re[0] != 0:
            msg.raise_cmd('%s failed' % lastcmd)
        return

    def checkGraphEnv(self, dir):
        msg.log("start checkGraphEnv")
        allFiles = os.listdir(dir)
        if 'ReadMe.txt' not in allFiles:
            msg.log('ReadMe.txt not exist, return False')
            return False
        try:
            graph = buildgraph.GraphEnv(dir + '/' + 'ReadMe.txt', dir)
        except:
            return False
        return graph.checkGraphEnv(self.checkScript)

    def checkModelEnv(self, dir):
        msg.log("start checkModelEnv")
        if 'ReadMe.txt' not in os.listdir(dir):
            msg.log("ReadMe.txt not exist in %s" % dir)
            return False
        try:
            mo = modelenv.Model(dir + '/' + 'ReadMe.txt', dir)
        except:
            return False
        return mo.checkModelFull()

    def startBuildModel(self, relm=False, refsn=False):
        destDir = self.targetDir + os.sep + self.targetName
        self.graphEnv = modelenv.Model(destDir + '/' + 'ReadMe.txt', destDir)
        self.graphEnv.setCheckScript(self.Path + self.checkScript)
        self.graphEnv.setModelDownloadDir(self.modelDir)
        self.graphEnv.setSourceDownloadDir(self.sourceDir)

        self.graphEnv.setVoc2dictDir(self.targetDir + self.voc2dict)
        self.graphEnv.setModelScriptDir(self.targetDir + self.modelScript)
        cf = ConfigParser.ConfigParser()
        cf.read(self.targetDir + os.sep + self.modelList)
        self.graphEnv.setModelConf(cf)

        df = ConfigParser.ConfigParser()
        df.read(self.targetDir + os.sep + self.sourceList)
        self.graphEnv.setSourceConf(df)

        if self.rebuildModelList != []:
            self.graphEnv.setRebuildModelList(self.rebuildModelList)
        if self.addCaidanModels != {}:
            self.graphEnv.setAddCaidanModels(self.addCaidanModels)

        self.graphEnv.printconf()
        self.graphEnv.setReBuildFsnFlag(self.reBuildFsn or refsn)
        self.graphEnv.setReBuildLmFlag(self.reBuildLm or relm)
        self.graphEnv.start2()

    def startBuildGraph(self, regraph=False, relmla=False):
        destDir = self.targetDir + os.sep + self.targetName
        self.graphEnv = buildgraph.GraphEnv(destDir + '/' + 'ReadMe.txt', destDir)
        self.graphEnv.setCheckScript(self.Path + self.checkScript)
        cf = ConfigParser.ConfigParser()
        cf.read(self.targetDir + os.sep + self.modelList)
        self.graphEnv.setModelConf(cf)
        df = ConfigParser.ConfigParser()
        df.read(self.targetDir + os.sep + self.sourceList)
        self.graphEnv.setSourceConf(df)

        self.graphEnv.setModelDownloadDir(self.modelDir)
        self.graphEnv.setSourceDownloadDir(self.sourceDir)

        self.graphEnv.setGraphScriptDir(self.targetDir + self.graphScript)
        self.graphEnv.setVoc2dictDir(self.targetDir + self.voc2dict)
        self.graphEnv.setModelScriptDir(self.targetDir + self.modelScript)
        if self.rebuildModelList != []:
            self.graphEnv.setRebuildModelList(self.rebuildModelList)
        if self.addCaidanModels != {}:
            self.graphEnv.setAddCaidanModels(self.addCaidanModels)
        self.graphEnv.printconf()
        self.graphEnv.start(regraph, relmla)

    def setGraphEnv(self):
        self.graphEnv.setCheckScript(self.Path + self.checkScript)
        cf = ConfigParser.ConfigParser()
        cf.read(self.targetDir + os.sep + self.modelList)
        self.graphEnv.setModelConf(cf)
        df = ConfigParser.ConfigParser()
        df.read(self.targetDir + os.sep + self.sourceList)
        self.graphEnv.setSourceConf(df)

        self.graphEnv.setModelDownloadDir(self.modelDir)
        self.graphEnv.setSourceDownloadDir(self.sourceDir)

        self.graphEnv.setGraphScriptDir(self.targetDir + self.graphScript)
        self.graphEnv.setVoc2dictDir(self.targetDir + self.voc2dict)
        self.graphEnv.setModelScriptDir(self.targetDir + self.modelScript)
        if self.rebuildModelList != []:
            self.graphEnv.setRebuildModelList(self.rebuildModelList)
        if self.addCaidanModels != {}:
            self.graphEnv.setAddCaidanModels(self.addCaidanModels)
        self.graphEnv.printconf()


    def changeConfigState(self):
        """change global Conf state"""
        msg.debug("change state to %s" % self.state)
        cf = ConfigParser.ConfigParser()
        cf.read(self.confFile)
        if cf.has_option('global', 'state') == True:
            cf.remove_option('global', 'state')
        cf.set('global', 'state', self.state)
        f = open(self.confFile, 'w')
        cf.write(f)
        f.close()

    def getScript(self):
        """check and download sources"""
        msg.debug("")
        if self.state == 0:
            self.downloadSources()
            self.state += 1
        else:
            self.checkDefaultSources()

    def getTargetEnv(self):
        """get target env"""
        msg.debug("get target env")
        if self.type == 'buildgraph':
            self.getGraph()
        else:
            self.getModel()
        self.state += 1

    def getTargetDepend(self):
        """get target dependent sources"""
        destDir = self.targetDir + os.sep + self.targetName
        if self.type == 'buildgraph':
            self.graphEnv = buildgraph.GraphEnv(destDir + '/' + 'ReadMe.txt', destDir)
        else:
            self.graphEnv = modelenv.Model(destDir + '/' + 'ReadMe.txt', destDir)
        self.setGraphEnv()
        if self.type != 'buildgraph':
            self.graphEnv.setReBuildFsnFlag(self.reBuildFsn)
            self.graphEnv.setReBuildLmFlag(self.reBuildLm)
        self.graphEnv.getDependSources()
        self.state += 1

    def getTarget(self):
        """build target"""
        msg.debug("get target")
        destDir = self.targetDir + os.sep + self.targetName
        if self.type == 'buildgraph':
            self.graphEnv = buildgraph.GraphEnv(destDir + '/' + 'ReadMe.txt', destDir)
        else:
            self.graphEnv = modelenv.Model(destDir + '/' + 'ReadMe.txt', destDir)
        self.setGraphEnv()
        if self.type != 'buildgraph':
            self.graphEnv.setReBuildFsnFlag(self.reBuildFsn)
            self.graphEnv.setReBuildLmFlag(self.reBuildLm)
        self.graphEnv.getTarget()
        self.state += 1
    
    def process(self):
        """process depending on self.state"""
        bs = self.state
        self.getScript()
        ps = self.state
        if bs != ps:
            self.changeConfigState()
        cont = self.continous

        if cont == False and bs != ps:
            return

        if self.state == 1:
            self.getTargetEnv()
            self.changeConfigState()
            if cont == False:
                return
        if self.state == 2:
            self.getTargetDepend()
            self.changeConfigState()
            if cont == False:
                return
        if self.state == 3:
            self.getTarget()
            self.changeConfigState()
            if cont == False:
                return


#self.changeConfigFile()


def Usage():
    print 'get_source.py usage:'
    print '-h, --help: print help message'
    print '-c, --config: set config file'
    print '-l, --logfile: set log file'
    print '-e, --email: set email addr'
    print '-v, --version: print version'


def Version():
    print 'get_source.py 1.0.0.0'


def main(argv):
    conf = ''
    email = 'quanzongfeng@baidu.com'
    logfile = 'temp_log_file'
    try:
        opts, args = getopt.getopt(argv[1:], 'hvc:l:e:', ['config=', 'email=', 'logfile=', 'help', 'version'])
    except getopt.GetoptError as err:
        print str(err)
        Usage()
        sys.exit(2)
    for o, a in opts:
        print o, a
        if o in ('-h', '--help'):
            Usage()
            sys.exit(1)
        elif o in ('-v', '--version'):
            Version()
            sys.exit(0)
        elif o in ('-c', '--config'):
            conf = a
        elif o in ('-l', '--logfile'):
            logfile = a
        elif o in ('-e', '--email'):
            email = a
        else:
            print 'unhandled option'
            Usage()
            sys.exit(3)
    if logfile != '':
        logfile = os.path.realpath(logfile)
        msg.set_log_file(logfile)
    if conf == '':
        print "no config file"
        Usage()
        sys.exit(4)

    print email
    print logfile
    print conf
    try:
        tn = TargetConf(conf)
        tn.processRebuildModelList()
        tn.printconf()
        tn.process()
#        tn.downloadSources()
#        if tn.type == 'buildgraph':
#            tn.getGraph()
#            tn.startBuildGraph()
#        else:
#            tn.getModel()
#            tn.startBuildModel()
    except:
        msg.except_msg(email)
        sys.exit()
    msg.send_log("succeed", email)


if __name__ == '__main__':
    main(sys.argv)

#/* vim: set expandtab ts=4 sw=4 sts=4 tw=100: */
