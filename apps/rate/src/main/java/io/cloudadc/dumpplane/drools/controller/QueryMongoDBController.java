package io.cloudadc.dumpplane.drools.controller;

import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import org.bson.Document;

import com.mongodb.client.MongoClient;
import com.mongodb.client.MongoClients;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;

import io.cloudadc.dumpplane.drools.model.NginxConfigDirective;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;

@RestController
@Tag(name = "Pipeline Data Store Query", description = "Pipeline Data Store Query")
public class QueryMongoDBController {
	
	private static MongoClient client = null;
	
	private static MongoClient newClient() {
		if (null == client) {
			client = MongoClients.create(System.getProperty("db.connection.mongodb", "mongodb://127.0.0.1:27017"));
		}
		return client;
	}
	
	@RequestMapping(value = "/data/query/workers", method = RequestMethod.GET, produces = "application/json")
	@Operation(summary = "List all worker process and connections", description = "List all worker process and connections")
	public List <NginxConfigDirective> list_all_worker_process_event() {
		
		MongoDatabase db = newClient().getDatabase("nginx");
		MongoCollection<Document> directive = db.getCollection("configurations_nginx_conf_directive");
		
		List<Document>  pipleline = Arrays.asList(new Document("$group", new Document("_id", "$ngxHost")));
		
		List<Document> result = directive.aggregate(pipleline).into(new ArrayList<>());
		
		List <NginxConfigDirective> results = new ArrayList<>();
		for (Document document : result) {
			String ngxHost = document.get("_id").toString();
			List<Document> worker_process = Arrays.asList(new Document("$match", 
				    new Document("$and", Arrays.asList(new Document("conf_directive.directive", "worker_processes"), 
			        new Document("ngxHost", ngxHost)))));
			List<Document> events = Arrays.asList(new Document("$match", 
				    new Document("$and", Arrays.asList(new Document("conf_directive.directive", "events"), 
			        new Document("ngxHost", ngxHost)))));
			List<Document> result_process = directive.aggregate(worker_process).into(new ArrayList<>());
			List<Document> result_connections = directive.aggregate(events).into(new ArrayList<>());
			
			String dumpFileName = null;
			String conf_file = null;
			String worker_processes = null;
			Integer worker_connections = null;
			if (result_process.size() > 0) {
				dumpFileName = result_process.get(0).getString("dumpFileName");
				conf_file = result_process.get(0).getString("conf_file");
				Document doc  = result_process.get(0).get("conf_directive", Document.class);
				worker_processes = (String) doc.get("args", ArrayList.class).get(0);
			}
			
			if(result_connections.size() > 0) {
				dumpFileName = result_connections.get(0).getString("dumpFileName");
				conf_file = result_connections.get(0).getString("conf_file");
				Document doc = result_connections.get(0).get("conf_directive", Document.class);
				Document subdoc = (Document) doc.get("block", ArrayList.class).get(0);
				worker_connections = Integer.parseInt((String)subdoc.get("args", ArrayList.class).get(0));
			}
			results.add(new NginxConfigDirective(ngxHost, dumpFileName, conf_file, worker_processes, worker_connections));
		}
			
		return results;
	}

}
