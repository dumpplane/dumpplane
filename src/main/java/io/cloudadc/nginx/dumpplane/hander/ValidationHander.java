package io.cloudadc.nginx.dumpplane.hander;

import java.nio.file.Paths;

import io.cloudadc.nginx.dumpplane.model.Configuration;

/**
 * Validation the crossplane result and dumpple result
 * 
 * @author ksong
 *
 */
public class ValidationHander extends AbstractHander {
	
	public static ValidationHander newInstance() {
		return new ValidationHander();
	}
	

	public ValidationHander() {
		super(null);
	}

	@Override
	public void execute(Configuration config) throws Exception {
		
		config.getCrossplane().getConfig().forEach(c -> {
			
			String prefix = Paths.get(config.getDiskPath(), config.getDumpFileName()).toString();
			
			c.setFile(c.getFile().replace(prefix, config.getBasePath()));
		});
	}

}
