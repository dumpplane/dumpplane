package io.cloudadc.dumpplane.drools.controller;

import java.util.ArrayList;
import java.util.List;

import org.kie.api.runtime.KieContainer;
import org.kie.api.runtime.KieSession;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

import io.cloudadc.dumpplane.drools.model.NginxConfigDirectiveFact;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;

@RestController
@Tag(name = "Nginx Configuration Validation", description = "Nginx Configuration Validation")
public class NginxConfigurationController {
	
	Logger log = LoggerFactory.getLogger(NginxConfigurationController.class);
	
	private final KieContainer kieContainer;
	
	private final QueryMongoDBController dbQuery;

	public NginxConfigurationController(KieContainer kieContainer) {
		this.kieContainer = kieContainer;
		this.dbQuery = new QueryMongoDBController();
	}
	
	@RequestMapping(value = "/rate/performance/tuning", method = RequestMethod.GET, produces = "application/json")
	@Operation(summary = "Verifiy performance tuning in nginx.conf", description = "Verifiy performance tuning in nginx.conf")
	public List<NginxConfigDirectiveFact> getQuestions() {
		
		List<NginxConfigDirectiveFact> results = new ArrayList<>();
		
		dbQuery.list_all_worker_process_event().forEach(d -> {
			if(d.getWorker_processes() != null && d.getWorker_connections() != null) {
				results.add(new NginxConfigDirectiveFact(d.getNgxHost(),d.getDumpFileName(), d.getConf_file(), d.getWorker_processes(), d.getWorker_connections()));
			}
		});
		
		KieSession kieSession = kieContainer.newKieSession();
		results.forEach(fact -> {
			kieSession.insert(fact);
		});
        
        kieSession.fireAllRules();
        kieSession.dispose();
        return results;
	}
}
