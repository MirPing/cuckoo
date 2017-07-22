
Notes: 
    CWD --- we use the so-called Cuckoo Working Directory (aka "CWD")

setup.py
    --- ��ȡ cuckoo/data/monitor/�µ�latest�ļ�  ---""" the monitoring binaries """
    --- ��ȡ MANIFEST.in�ļ���������������
    --- githash()   """Extracts the current Git hash.""" ��д��cuckoo/data-private/.cwd�ļ��У�û����д��
    --- update_hashes() """Provide hashes for our CWD migration process.""" �����cuckoo/data�������ļ���hashֵ��д��cuckoo/data-private/cwd/hashes.txt�ļ���
    --- do_setup(**kwargs) ����setuptools.setup(**kwargs)���д��� �����кܶ�����İ�װ��  
        ���е�    entry_points={
                            "console_scripts": [
                                "cuckoo = cuckoo.main:main",
                            ],
                  },
                  """ �� console_scripts �£�ÿһ�ж���һ������̨�ű����Ⱥ���ߵĵ��ǽű������ƣ��ұߵ��� Click ����ĵ���·����"""
                  packages=[
                    "cuckoo",
                  ],
                  


cuckoo/main.py
    --- main(ctx, debug, quiet, nolog, maxcount, user, cwd)
        --- cuckoo.misc.decide_cwd(cwd)  """Decides and sets the CWD, optionally checks if it's a valid CWD."""
                                         """Default value ("~/.cuckoo")"""
            --- set_cwd(dirpath, raw=cwd)  """��������ȫ�ֱ�����ֵ --- cuckoo _raw��·��~./cuckoo��_root��·��"""                                               
        --- cuckoo.misc.drop_privileges(user)      """Drops privileges to selected user.
                                                      @param username: drop privileges to this username
                                                   """                                                                                   
        --- cuckoo_init(level, ctx)     """Initialize Cuckoo configuration.
                                           @param quiet: enable quiet mode.
                                        """                                           
            --- cuckoo.common.logo()      """Cuckoo asciiarts.
                                             @return: asciiarts array.
                                           """
            --- cuckoo_create(ctx.user, cfg)  """Create a new Cuckoo Working Directory."""
                --- """����~./cuckoo cwd ����Ŀ¼ ��cuckoo/data�µ�Ŀ¼��copy����������.pyc�ļ���copy"""
                --- cuckoo.core.init/write_supervisor_conf(username or getuser())  """Writes supervisord.conf configuration file if it does not exist yet."""
                --- cuckoo.core.init/write_cuckoo_conf(cfg=cfg) #Merge any provided configuration with the defaults and emit their values.  
                """��config.py�ļ��е����÷ֱ�д����ͬ���ļ���ȥ"""  
                
                #-------------�����ǵ�һ���������������飬�������ٴε��õ�ʱ������������
                
                --- cuckoo.core.startup.init_console_logging(level)  """Initializes logging only to console and database."""            
                --- cuckoo.core.startup.check_configs()      """Checks if config files exist.
                                                                @raise CuckooStartupError: if config files do not exist.
                                                             """      
                --- cuckoo.core.startup.check_version()   """Checks version of Cuckoo."""
                --- cuckoo.core.startup.init_logging(level)   """Initializes logging."""
                --- cuckoo.core.database.Database().connect()  """Connect to the database backend."""
                --- cuckoo.misc.load_signatures()      """Loads additional Signatures from the Cuckoo Working Directory.
                                                          This method is quite hacky in the sense that it magically imports
                                                          Signatures from an arbitrary directory - one that doesn't belong to the
                                                          Cuckoo package directly.
                                                          Furthermore this method provides backwards compatibility with older
                                                          Signatures which rely on the "lib.cuckoo.common.abstracts" import, one
                                                          that can now be accessed as "cuckoo.common.abstracts".
                                                        """
                --- cuckoo.core.startup.init_tasks()  """Check tasks and reschedule uncompleted ones."""
                --- cuckoo.core.startup.init_yara(True)  """Generates index for yara signatures."""
                --- cuckoo.core.startup.init_binaries()      """Inform the user about the need to periodically look for new analyzer    binaries. These include the Windows monitor etc."""
                --- cuckoo.core.startup.init_rooter()      """If required, check if the rooter is running and if we can connect to it. The default configuration doesn't require the rooter to be ran."""   
                --- cuckoo.core.startup.init_routing()    """Initialize and check whether the routing information is correct."""
                --- cuckoo.signatures ��ȡ�����������        
        --- cuckoo_main(maxcount)      """Cuckoo main loop.
                                          @param max_analysis_count: kill cuckoo after this number of analyses
                                       """
            --- cuckoo.core.resultserver.ResultServer()     """Result server. Singleton!
                                                              This class handles results coming back from the analysis machines.
                                                           """  
            --- cuckoo.core.scheduler.Scheduler(max_analysis_count)     """Tasks Scheduler.
                                                                           This class is responsible for the main execution loop of the tool. It
                                                                           prepares the analysis machines and keep waiting and loading for new analysis tasks.
                                                                           Whenever a new task is available, it launches AnalysisManager which will
                                                                           take care of running the full analysis process and operating with the assigned analysis machine.
                                                                        """
                --- cuckoo.core.scheduler.Scheduler.start()  """Start scheduler."""
                    --- self.initialize()   """Initialize the machine manager."""
                        --- machinery = cuckoo.machinery.plugins[machinery_name]()#machinery_name == virtualbox
                                --- plugins = enumerate_plugins(__file__, "cuckoo.machinery", globals(), Machinery, as_dict=True)
                                    --- enumerate_plugins(dirpath, module_prefix, namespace, class_,attributes={}, as_dict=False):          """Import plugins of type `class` located at `dirpath` into the
                                                    `namespace` that starts with `module_prefix`. If `dirpath` represents a
                                                    filepath then it is converted into its containing directory. The
                                                    `attributes` dictionary allows one to set extra fields for all imported
                                                    plugins. Using `as_dict` a dictionary based on the module name is returned.
                                              """
                                              """����cuckoo.machineryĿ¼�����е�pythonģ��"""
                                              """���ص�������cuckoo.machinery��abstracts.py��Machinery�����������"""
                                              
                    --- analysis = AnalysisManager(task.id, errors)
                    --- analysis.start() #AnalysisManager�̳���Threading��
                                                                 """Analysis Manager.
                                                                    This class handles the full analysis process for a given task. It takes
                                                                    care of selecting the analysis machine, preparing the configuration and
                                                                    interacting with the guest agent and analyzer components to launch and
                                                                    complete the analysis and store, process and report its results.
                                                                 """
                            --- run()  """Run manager thread."""
                                --- self.launch_analysis()  """Start analysis."""
                                    --- self.init()  """"Initialize the analysis.""" #��storge/analysis Ŀ¼�´���task.id��Ŀ¼
                                        --- self.store_task_info() """grab latest task from db (if available) and update self.task"""
                                    --- self.acquire_machine() """Acquire an analysis machine from the pool of available ones."""
                                    --- ResultServer().add_task(self.task, self.machine)   """Register a task/machine with the ResultServer."""## At this point we can tell the ResultServer about it.
                                    --- GuestManager(self.machine.name, self.machine.ip,self.machine.platform, self.task.id, self)"""This class represents the new Guest Manager. It operates on the new
    Cuckoo Agent which features a more abstract but more feature-rich API.""" # Initialize the guest manager.
                                    --- self.aux = RunAuxiliary(self.task, self.machine, self.guest_manager) """Auxiliary modules manager."""#self.aux�Ķ���û���
                                        --- self.aux.start()  #cuckoo.auxiliary.plugins�а�����ģ���������
                                    --- options = self.build_options()  """Generate analysis options.@return: options dict."""
                                    --- machinery.start(self.machine.label, self.task)  #virtualbox.start()
                                            """Start a virtual machine.
                                            @param label: virtual machine name.
                                            @param task: task object.
                                            @raise CuckooMachineError: if unable to start.
                                            """
                                            --- self.restore(label, machine) """Restore a VM to its snapshot."""









analyzer.py       """
                     Cuckoo Windows Analyzer.
                     This class handles the initialization and execution of the analysis
                     procedure, including handling of the pipe server, the auxiliary modules and
                     the analysis packages.
                  """                                            
        --- class Analyzer(object):
            --- run()          """
                                    Run analysis.
                                    @return: operation status.
                               """
                --- self.prepare() """Prepare env for analysis."""
                    --- grant_privilege("SeDebugPrivilege")
                        grant_privilege("SeLoadDriverPrivilege")         # Get SeDebugPrivilege for the Python process. It will be needed in order to perform the injections.
                    --- init_logging()  # Initialize logging.
                    --- self.config = Config(cfg="analysis.conf") # Parse the analysis configuration file generated by the agent.
                    --- Process.set_config(self.config) # Pass the configuration through to the Process class.
                    ---  self.command_pipe = PipeServer(PipeDispatcher, self.config.pipe, message=True,dispatcher=CommandPipeHandler(self))        # Initialize and start the Command Handler pipe server. This is going to be used for communicating with the monitored processes.
                    --- self.log_pipe_server = PipeServer(PipeForwarder, self.config.logpipe, destination=destination)    # Initialize and start the Log Pipe Server - the log pipe server will open up a pipe that monitored processes will use to send logs to before they head off to the host machine.
                
                --- lib.core.packages.choose_package()   # If the analysis target is a file, we choose the package according to the file format.
                --- __import__() # Try to import the analysis package.
                --- lib.common.abstracts.Package() # Initialize the package parent abstract.
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                                
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                                         
                                         
                                         
                                         