package io.cloudadc.dumpplane.drools.model;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;

/**
 * 
 *  Dumpplane represent the nginx -T output, which is s group of configuration block, Dumpplane is one of block
 * 
 * @author ksong
 *
 */
public class Dumpplane implements Serializable {
	
	private static final long serialVersionUID = -5526117033798890872L;

	private Integer conf_num;
	
	private List<Dumpplane> rawconfig = new ArrayList<>();
	
	public Dumpplane() {
		
	}

	public Dumpplane(Integer conf_num, List<Dumpplane> rawconfig) {
		super();
		this.conf_num = conf_num;
		this.rawconfig = rawconfig;
	}

	public Integer getConf_num() {
		return conf_num;
	}

	public void setConf_num(Integer conf_num) {
		this.conf_num = conf_num;
	}

	public List<Dumpplane> getRawconfig() {
		return rawconfig;
	}

	public void setRawconfig(List<Dumpplane> rawconfig) {
		this.rawconfig = rawconfig;
	}

}
