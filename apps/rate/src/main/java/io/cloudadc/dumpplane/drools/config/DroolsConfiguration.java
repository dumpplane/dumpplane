package io.cloudadc.dumpplane.drools.config;

import java.io.File;
import java.nio.file.Paths;

import org.kie.api.KieServices;
import org.kie.api.builder.KieBuilder;
import org.kie.api.builder.KieFileSystem;
import org.kie.api.builder.KieModule;
import org.kie.api.runtime.KieContainer;
import org.kie.internal.io.ResourceFactory;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class DroolsConfiguration {
	
	Logger log = LoggerFactory.getLogger(DroolsConfiguration.class);
	
	private final KieServices kieServices = KieServices.Factory.get();
	
	@Bean
    public KieContainer getKieContainer() {
		
		KieFileSystem kieFileSystem = kieServices.newKieFileSystem();
		
		File rule = Paths.get(System.getProperty("rate.algorithm.sheets", "rules/nginx-ops.xlsx")).toFile();
		log.info("load rule  " + rule);
		kieFileSystem.write(ResourceFactory.newFileResource(rule));
		
		//kieFileSystem.write(ResourceFactory.newClassPathResource("rules/test.xls"));
		KieBuilder kb = kieServices.newKieBuilder(kieFileSystem);
		kb.buildAll();
		KieModule kieModule = kb.getKieModule();
		return kieServices.newKieContainer(kieModule.getReleaseId());
	}

}
