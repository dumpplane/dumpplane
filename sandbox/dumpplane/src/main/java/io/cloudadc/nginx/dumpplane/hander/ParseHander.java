package io.cloudadc.nginx.dumpplane.hander;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Base64;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import io.cloudadc.nginx.dumpplane.model.Configuration;
import io.cloudadc.nginx.dumpplane.model.Dumpplane;


public class ParseHander extends AbstractHander {
	
	private List<Configuration> list = new ArrayList<>();
	
	
	public static ParseHander newInstance(File file) throws Exception {
		return new ParseHander(file);
	}
	
	public ParseHander(File file) throws Exception {
		super(file);
	}

	@Override
	public void execute() throws Exception {
		
		parse(file);
		
	}

	private void parse(File targetFile) {
		
		//System.out.println("parse " + targetFile);
		
		if(targetFile.isDirectory()) {
			for(File f : targetFile.listFiles()) {
				parse(f);
			}

		} else {
			
			Configuration config = new Configuration();
			config.setDumpFileName(targetFile.getName());
			config.setNgxHost(extractHost(config.getDumpFileName()));
			config.setDiskPath(Paths.get(System.getProperty("user.home"), DUMP_PATH, DISK_PATH).toString());
			
			String configPath = null;

			try {
	            BufferedReader reader = new BufferedReader(new FileReader(targetFile));
	            String line = reader.readLine();
	            BufferedWriter writer = null;
	            StringBuffer sb = null;
	            while (line != null) {
	                if (line.startsWith("#") && line.endsWith(":")) {
	                	if (writer != null) {
	                        writer.close();
	                    }
	                	addBlock(sb, configPath, config);
	                    configPath = line.substring(line.indexOf("/"), line.length() -1);
	                    
	                    String basePath = configPath.substring(0, configPath.lastIndexOf("/"));
	                    if(config.getBasePath() == null || config.getBasePath().length() ==0) {
	        				config.setBasePath(basePath);
	        			} else if (basePath.length() <= config.getBasePath().length()) {
	        				config.setBasePath(basePath);
	        			}
	                    
	                    sb = new StringBuffer();
	                } else {
	                	// crossparse tried to load mime.types
	                	if(line.contains("/etc/nginx/mime.types")) {
	                		line = line.replace("/etc/nginx/mime.types", "mime.types");
	                	}
	                	
	                	if(line.contains(config.getBasePath())) {
	                		line = line.replace(config.getBasePath() + "/", "");
	                	}
	                	
	                    sb.append(line).append("\n");
	                }
	                line = reader.readLine();
	            }
	            addBlock(sb, configPath, config);
	            reader.close();
	        } catch (IOException e) {
	            throw new RuntimeException(e);
	        }
			
			list.add(config);
		}
		
		
		
		//return ;
		
	}

	private void addBlock(StringBuffer sb, String configPath, Configuration config) {

		if(sb != null && configPath != null) {
			String originalString = sb.toString();
			//String encodedString = Base64.getEncoder().encodeToString(originalString.getBytes());
			Dumpplane block = new Dumpplane(configPath, originalString);
			config.addDump(block);
			sb = null;
			configPath = null;
		}
	}

	private String extractHost(String dumpFileName) {
		
		String regex = "\\b(?:\\d{1,3}\\.){3}\\d{1,3}\\b";
		Pattern pattern = Pattern.compile(regex);
		Matcher matcher = pattern.matcher(dumpFileName);
		if(matcher.find()) {
			return matcher.group();
		} else if (dumpFileName.contains("_")) {
			return dumpFileName.substring(dumpFileName.indexOf("_") + 1);
		}
		return dumpFileName;
	}
	
	public List<Configuration> getConfigs() {
		return list;
	}

	@Override
	public void close() throws Exception {
		this.list = null;
	}

}
