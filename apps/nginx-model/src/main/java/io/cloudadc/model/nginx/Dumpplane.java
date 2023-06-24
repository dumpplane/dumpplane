package io.cloudadc.model.nginx;

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
	
	private List<RawConfig> rawconfig = new ArrayList<>();
	
	public Dumpplane() {
		
	}

	public Dumpplane(Integer conf_num, List<RawConfig> rawconfig) {
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

	public List<RawConfig> getRawconfig() {
		return rawconfig;
	}

	public void setRawconfig(List<RawConfig> rawconfig) {
		this.rawconfig = rawconfig;
	}

}
