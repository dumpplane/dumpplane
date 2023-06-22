package io.cloudadc.nginx.dumpplane.hander;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.List;

import org.bson.Document;
import org.bson.conversions.Bson;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.core.exc.StreamWriteException;
import com.fasterxml.jackson.databind.DatabindException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.mongodb.client.MongoClient;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;
import com.mongodb.client.model.Filters;
import com.mongodb.client.model.ReplaceOptions;
import com.mongodb.client.result.UpdateResult;

import co.elastic.clients.elasticsearch.ElasticsearchClient;
import co.elastic.clients.elasticsearch._types.ElasticsearchException;
import co.elastic.clients.elasticsearch.core.IndexResponse;
import io.cloudadc.nginx.dumpplane.model.Configuration;

public class DumpPersistHander extends AbstractHander {
	
	public static DumpPersistHander newInstance() {
		return new DumpPersistHander();
	}

	public DumpPersistHander() {
		super(null);
	}

	@Override
	public void execute(Configuration config) throws Exception {
		
		System.out.println(objectToDocument(config));

	}

	@Override
	public void execute(List<Configuration> list) throws Exception {
		for(Configuration c : list) {
			execute(c);
		}
	}
	
	public void dumpToFile(Configuration config, File file) throws StreamWriteException, DatabindException, IOException {
		
		ObjectMapper mapper = new ObjectMapper();
		
		FileWriter writer = new FileWriter(file, false);
		
		mapper.writeValue(writer, config);
		
		writer.close();
		
	}

	public void dumpToMongoDB(Configuration config, MongoClient mongoClient) throws JsonProcessingException {

		MongoDatabase database = mongoClient.getDatabase(DB_NAME);
        MongoCollection<Document> collection = database.getCollection("configurations");
        
        Document doc = Document.parse(objectToDocument(config));
        
        Bson query = Filters.eq("dumpFileName", config.getDumpFileName());
        
        ReplaceOptions opts = new ReplaceOptions().upsert(true);
        
        UpdateResult result = collection.replaceOne(query, doc, opts);
        
        if(result.wasAcknowledged()) {
        	System.out.println("write " + config.getDumpFileName() + " to DB was acknowledged, matched count: " + result.getMatchedCount());
        }
	}

	public void dumpToElastic(Configuration config, ElasticsearchClient client) throws ElasticsearchException, IOException {

		IndexResponse response = client.index(i -> i
			    .index("nginx")
			    .id(config.getDumpFileName())
			    .document(config)
			);
		
		System.out.println("Indexed nginx config on host " + config.getNgxHost() + " with version " + response.version());
	}

	
}
