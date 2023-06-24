package io.cloudadc.model.nginx;

public class RawConfig {
	
	private String filepath;
	
	private String dirname;
	
	private String filename;
	
	private String separator;
	
	private String content;
	
	public RawConfig() {
		
	}

	public RawConfig(String filepath, String dirname, String filename, String separator, String content) {
		super();
		this.filepath = filepath;
		this.dirname = dirname;
		this.filename = filename;
		this.separator = separator;
		this.content = content;
	}

	public String getFilepath() {
		return filepath;
	}

	public void setFilepath(String filepath) {
		this.filepath = filepath;
	}

	public String getDirname() {
		return dirname;
	}

	public void setDirname(String dirname) {
		this.dirname = dirname;
	}

	public String getFilename() {
		return filename;
	}

	public void setFilename(String filename) {
		this.filename = filename;
	}

	public String getSeparator() {
		return separator;
	}

	public void setSeparator(String separator) {
		this.separator = separator;
	}

	public String getContent() {
		return content;
	}

	public void setContent(String content) {
		this.content = content;
	}

}
