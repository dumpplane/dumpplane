package io.cloudadc.dumpplane.drools.model;

public class NginxConfigDirective {
	
	private String ngxHost;
	private String dumpFileName ;
	private String conf_file ;
	private String worker_processes ;
	private Integer worker_connections ;
	
	public NginxConfigDirective() {}
	
	public NginxConfigDirective(String ngxHost, String dumpFileName, String conf_file, String worker_processes,
			Integer worker_connections) {
		super();
		this.ngxHost = ngxHost;
		this.dumpFileName = dumpFileName;
		this.conf_file = conf_file;
		this.worker_processes = worker_processes;
		this.worker_connections = worker_connections;
	}

	public String getNgxHost() {
		return ngxHost;
	}

	public void setNgxHost(String ngxHost) {
		this.ngxHost = ngxHost;
	}

	public String getDumpFileName() {
		return dumpFileName;
	}

	public void setDumpFileName(String dumpFileName) {
		this.dumpFileName = dumpFileName;
	}

	public String getConf_file() {
		return conf_file;
	}

	public void setConf_file(String conf_file) {
		this.conf_file = conf_file;
	}

	public String getWorker_processes() {
		return worker_processes;
	}

	public void setWorker_processes(String worker_processes) {
		this.worker_processes = worker_processes;
	}

	public Integer getWorker_connections() {
		return worker_connections;
	}

	public void setWorker_connections(Integer worker_connections) {
		this.worker_connections = worker_connections;
	}
    
    


}
