package io.cloudadc.dumpplane.drools.model;

public class NginxConfigDirectiveFact extends NginxConfigDirective {
	
	private String results;
	
	public NginxConfigDirectiveFact() {
		
	}
	
	public NginxConfigDirectiveFact(String ngxHost, String dumpFileName, String conf_file, String worker_processes, Integer worker_connections) {
		super(ngxHost, dumpFileName, conf_file, worker_processes, worker_connections);
	}

	public String getResults() {
		return results;
	}

	public void setResults(String results) {
		this.results = results;
	}

}
