package org.ird;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.URL;

import de.uni_mannheim.informatik.dws.melt.matching_base.external.cli.process.ProcessOutputAlignmentCollector;

/**
 * Wrapper for the external Python matcher.
 * RDFlib is required in python environment.
 */
public class CommandPythonMatcher {
    
    private String source;
    private String target;
    
    public CommandPythonMatcher(String source, String target) {
		this.source = source;
		this.target = target;
    }
    
    protected String getCommand() {
        String command = "python " + getAbsolutePathofResources("oaei-resources/pythonMatcher.py") + " --source ${source} --target ${target}";
        command = command.replace("${source}", this.source);
        command = command.replace("${target}", this.target);
        
//        command = "python3.8 <<< print('Hi')"; //  'file:///tmp/alignment_09k6uu1e.rdf'";
        return command;
    }
    
    /**
     * Returns the python command which is extracted from {@code file oaei-resources/python_command.txt}.
     * @return The python executable path.
     */
    private String getAbsolutePathofResources(String file){
        return new File(file).getAbsolutePath();
    }
    
    public String runCommand() {
    	String result = null;
    	try {
			result = this.match(this.source, this.target);
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return result;
    }
    
    /** ********/
    
    protected boolean isUsingStdOut(){
        return true;
    }
    
    @SuppressWarnings("unused")
    private void showFileContent(String file) {
        BufferedReader br;
        try {
            br = new BufferedReader(new FileReader(file));
            String line;
            try {
                while ((line = br.readLine()) != null) {
                  System.out.println(line);
                }
            } catch (IOException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }
        } catch (FileNotFoundException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
    }
   
    public String match(String source, String target) {
        //this.showFileContent(source);
        //this.showFileContent(target);
        ProcessOutputAlignmentCollector alignmentCollector = new ProcessOutputAlignmentCollector();
        StringBuilder output = new StringBuilder("");
    	try {
    		System.out.println(getCommand());
            Process process = Runtime.getRuntime().exec(getCommand()); // "echo file:///tmp/alignment_vdeyzwa1.rdf"
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            String line;
            System.out.println("Start get output of subprocess 0%");
            while ((line = reader.readLine()) != null) {
                output.append(line + "\n");
                System.out.println(line + "\n");
                alignmentCollector.processOutput(line);
            }
            System.out.println("End get output of subprocess 100%");
            int exitVal = process.waitFor();
            if (exitVal == 0) {
            	URL detectedURL = alignmentCollector.getURL();
                System.out.println("**************************** The Output is ******************************");
                // System.out.println(output);
                String outputFile = this.getAbsolutePathofResources("oaei-resources") + detectedURL.getFile();
                System.out.println("Detected file : " + outputFile);
                // this.showFileContent(outputFile);
                return outputFile;
            } else {
            	System.out.println("**************************** Error : " + exitVal + " ******************************");
            }
        }
        catch (IOException e) {
            e.printStackTrace();
        }
        catch (InterruptedException e) {
            e.printStackTrace();
        }
    	
    	return output.toString();
    }
    
//    public static void main(String[] args) {
//    	String source = new File("oaei-resources/inputs/spaten_hobbit/source.nt").getAbsolutePath();
//    	String target = new File("oaei-resources/inputs/spaten_hobbit/target.nt").getAbsolutePath();
//    	CommandPythonMatcher cpm1 = new CommandPythonMatcher(source, target);
//    	cpm1.runCommand();
//    }
}

