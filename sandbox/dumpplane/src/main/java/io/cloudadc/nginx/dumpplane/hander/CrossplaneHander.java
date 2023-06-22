package io.cloudadc.nginx.dumpplane.hander;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;

import com.fasterxml.jackson.databind.ObjectMapper;

import io.cloudadc.nginx.dumpplane.model.Configuration;
import io.cloudadc.nginx.dumpplane.model.Crossplane;

/**
 * 
 * Load the crossplane parsed jSON to object, and set to Configuration
 * 
 * @author ksong
 *
 */
public class CrossplaneHander extends AbstractHander {
	
	/**
	 * @param file - crossplane parsed jSON file
	 * @return
	 */
	public static CrossplaneHander newInstance(File file) {
		return new CrossplaneHander(file);
	}

	public CrossplaneHander(File file) {
		super(file);
	}
	
    public void execute(Configuration config) throws IOException {
		
		String rawCrossFile = readStreamFromfile(getFile());
				
		ObjectMapper mapper = new ObjectMapper();
		Crossplane crossplane = mapper.readValue(rawCrossFile.getBytes(), Crossplane.class);
		config.setCrossplane(crossplane);
		
	}

	private String readStreamFromfile(File file) throws IOException {
		
		byte[] bytes = new byte[(int) file.length()];
		FileInputStream fis = new FileInputStream(file);
		fis.read(bytes);
		String fileContent = new String(bytes, "UTF-8"); 
		fis.close();
		
		return fileContent;
	}


}
