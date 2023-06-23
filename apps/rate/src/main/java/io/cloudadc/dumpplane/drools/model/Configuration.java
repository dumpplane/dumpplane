package io.cloudadc.dumpplane.drools.model;

import java.io.Serializable;

public class Configuration implements Serializable {
	
	private static final long serialVersionUID = 5338581958567066631L;

	private String dumpFileName;
	
	private String ngxHost;
	
	private String basePath;
	
	private String diskPath;
	
	private Dumpplane dumpplane ;
	
	private Crossplane crossplane;
	
	public Configuration() {
		
	}

	public Configuration(String dumpFileName, String ngxHost) {
		super();
		this.dumpFileName = dumpFileName;
		this.ngxHost = ngxHost;
	}
	
	public Configuration(String dumpFileName, String ngxHost, String basePath, String diskPath) {
		super();
		this.dumpFileName = dumpFileName;
		this.ngxHost = ngxHost;
		this.basePath = basePath;
		this.diskPath = diskPath;
	}
	
	public Configuration(String dumpFileName, String ngxHost, String basePath, String diskPath, Dumpplane dumpplane) {
		super();
		this.dumpFileName = dumpFileName;
		this.ngxHost = ngxHost;
		this.basePath = basePath;
		this.diskPath = diskPath;
		this.dumpplane = dumpplane;
	}
	
	public Configuration(String dumpFileName, String ngxHost, String basePath, Dumpplane dumpplane, Crossplane crossplane) {
		super();
		this.dumpFileName = dumpFileName;
		this.ngxHost = ngxHost;
		this.basePath = basePath;
		this.dumpplane = dumpplane;
		this.crossplane = crossplane;
	}

	public String getDumpFileName() {
		return dumpFileName;
	}

	public void setDumpFileName(String dumpFileName) {
		this.dumpFileName = dumpFileName;
	}

	public String getNgxHost() {
		return ngxHost;
	}

	public void setNgxHost(String ngxHost) {
		this.ngxHost = ngxHost;
	}

	public String getBasePath() {
		return basePath;
	}

	public String getDiskPath() {
		return diskPath;
	}

	public void setDiskPath(String diskPath) {
		this.diskPath = diskPath;
	}

	public void setBasePath(String basePath) {
		this.basePath = basePath;
	}


	public Dumpplane getDumpplane() {
		return dumpplane;
	}

	public void setDumpplane(Dumpplane dumpplane) {
		this.dumpplane = dumpplane;
	}

	public Crossplane getCrossplane() {
		return crossplane;
	}

	public void setCrossplane(Crossplane crossplane) {
		this.crossplane = crossplane;
	}


}
