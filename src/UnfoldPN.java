//////////////////////////////////////////////////////////////////
//
//    Copyright (C) 2019  Universitat Politecnica de Catalunya
//
//    This library is free software; you can redistribute it and/or
//    modify it under the terms of the GNU Affero General Public
//    License as published by the Free Software Foundation; either
//    version 3 of the License, or (at your option) any later version.
//
//    This library is distributed in the hope that it will be useful,
//    but WITHOUT ANY WARRANTY; without even the implied warranty of
//    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
//    Affero General Public License for more details.
//
//    You should have received a copy of the GNU Affero General Public
//    License along with this library; if not, write to the Free Software
//    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
//
//    contact: Lluis Padro (padro@cs.upc.es)
//             Computer Science Department
//             Omega-320 - Campus Nord UPC
//             C/ Jordi Girona 31
//             08034 Barcelona.  SPAIN
//
////////////////////////////////////////////////////////////////


import org.jbpt.petri.NetSystem;
import org.jbpt.petri.Node;
import org.jbpt.petri.Place;
import org.jbpt.petri.Transition;
import org.jbpt.petri.unfolding.ProperCompletePrefixUnfolding;
import org.jbpt.petri.io.PNMLSerializer;

import java.util.HashMap;
import java.util.Scanner;

public class UnfoldPN {

    /// load PN from stdin (in plain text format generated by 'dump')

    private static NetSystem loadPetriNet() {
	NetSystem net = new NetSystem();
	HashMap<String, Place> places = new HashMap<String, Place>();
	HashMap<String, Transition> transitions = new HashMap<String, Transition>();
        
	Scanner input = new Scanner(System.in);
        while (input.hasNext()) {
            String line = input.nextLine();
	    String[] fields = line.split(" ");
	    if (fields[0].equals("PLACE")) {
		Place p = new Place();
                p.setId(fields[1]);
                p.setName(fields[2]);
		net.addNode(p);
		if (fields[3].equals("INITIAL")) net.getMarking().put(p,1);
		places.put(fields[1],p);
	    }
	    else if (fields[0].equals("TRANSITION")) {
		Transition t = new Transition();
                t.setId(fields[1]);
                t.setName(fields[2]);
		net.addNode(t);
		transitions.put(fields[1],t);
	    }
	    else if (fields[0].equals("ARC")) {
		if (places.containsKey(fields[1]) && transitions.containsKey(fields[2]))
		    net.addFlow(places.get(fields[1]), transitions.get(fields[2]));
		else if (transitions.containsKey(fields[1]) && places.containsKey(fields[2]))
		    net.addFlow(transitions.get(fields[1]), places.get(fields[2]));
	    }
        }        
        return net;
    }


    /// -- MAIN -- 
   
    public static void main(String[] args) throws Exception {
	
        NetSystem net = loadPetriNet();    
        ProperCompletePrefixUnfolding pcpu = new ProperCompletePrefixUnfolding(net);

        PNMLSerializer slz = new PNMLSerializer();
        System.out.println(slz.serializePetriNet(net));        
    }

}