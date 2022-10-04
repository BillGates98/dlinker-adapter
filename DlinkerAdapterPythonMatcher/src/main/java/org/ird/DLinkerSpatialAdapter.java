package org.ird;

import java.io.File;
import java.io.IOException;
import java.nio.ByteBuffer;
import java.util.logging.Level;

import org.apache.commons.io.FileUtils;
import org.hobbit.core.Commands;
import org.hobbit.core.components.AbstractSystemAdapter;
import org.hobbit.core.rabbit.RabbitMQUtils;
import org.hobbit.core.rabbit.SimpleFileReceiver;

import com.rabbitmq.client.ConsumerCancelledException;
import com.rabbitmq.client.ShutdownSignalException;

public class DLinkerSpatialAdapter {

//extends AbstractSystemAdapter {
//
//    protected File folder = new File("");
//    private SimpleFileReceiver sourceReceiver;
//    private SimpleFileReceiver targetReceiver;
//    private String receivedGeneratedDataFilePath;
//    private String dataFormat;
//    private String taskFormat;
//    private String resultsFile;
//
//    @Override
//    public void init() throws Exception {
//        System.out.println("Initializing DLinker test system...");
//        long time = System.currentTimeMillis();
//        super.init();
//        System.out.println("Super class initialized. It took " + (System.currentTimeMillis() - time) + "ms.");
//        time = System.currentTimeMillis();
//        sourceReceiver = SimpleFileReceiver.create(this.incomingDataQueueFactory, "source_file");
//        System.out.println("Receivers initialized. It took " + (System.currentTimeMillis() - time) + "ms.");
//        System.out.println("DLinker initialized successfully.");
//    }
//
//    @Override
//    public void receiveGeneratedData(byte[] data) {
//        try {
//        	System.out.println("Starting receiveGeneratedData..");
//
//            ByteBuffer dataBuffer = ByteBuffer.wrap(data);
//            dataFormat = RabbitMQUtils.readString(dataBuffer);
//            // read the file path
//            receivedGeneratedDataFilePath = RabbitMQUtils.readString(dataBuffer);
//
//            String[] receivedFiles = sourceReceiver.receiveData("./datasets/SourceDatasets/");
//            receivedGeneratedDataFilePath = "./datasets/SourceDatasets/" + receivedFiles[0];
//            System.out.println("Received data from receiveGeneratedData..");
//
//        } catch (IOException | ShutdownSignalException | ConsumerCancelledException | InterruptedException ex) {
//            java.util.logging.Logger.getLogger(DLinkerAdapter.class.getName()).log(Level.SEVERE, null, ex);
//        }
//
//    }
//
//    @Override
//    public void receiveGeneratedTask(String taskId, byte[] data) {
//    	System.out.println("Starting receiveGeneratedTask..");
//    	System.out.println("Task " + taskId + " received from task generator");
//        long time = System.currentTimeMillis();
//        try {
//
//            ByteBuffer taskBuffer = ByteBuffer.wrap(data);
//            // read the relation
//            String taskRelation = RabbitMQUtils.readString(taskBuffer);
//            System.out.println("DLinker version 1.0");
//            System.out.println("taskRelation " + taskRelation);
//            // read the target geometry
//            String targetGeom = RabbitMQUtils.readString(taskBuffer);
//            System.out.println("targetGeom " + targetGeom);
//            // read namespace
//            String namespace = RabbitMQUtils.readString(taskBuffer);
//            System.out.println("namespace " + namespace);
//            // read the file path
//            taskFormat = RabbitMQUtils.readString(taskBuffer);
//            System.out.println("Parsed task " + taskId + ". It took " + (System.currentTimeMillis() - time) + "ms.");
//            time = System.currentTimeMillis();
//
//            String receivedGeneratedTaskFilePath = null;
//            try {
//
//                targetReceiver = SingleFileReceiver.create(this.incomingDataQueueFactory,
//                        "task_target_file");
//                String[] receivedFiles = targetReceiver.receiveData("./datasets/TargetDatasets/");
//                receivedGeneratedTaskFilePath = "./datasets/TargetDatasets/" + receivedFiles[0];
//
//            } catch (Exception e) {
//            	System.out.println("Exception while trying to receive data. Aborting." + e.getMessage());
//            }
//            System.out.println("Received task data. It took " + (System.currentTimeMillis() - time) + "ms.");
//            time = System.currentTimeMillis();
//
//            System.out.println("Task " + taskId + " received from task generator");
//
//            this.resultsFile = this.pythonMatcherController(receivedGeneratedDataFilePath, receivedGeneratedTaskFilePath);
//            byte[][] resultsArray = new byte[1][];
//
//            resultsArray[0] = FileUtils.readFileToByteArray(new File(this.resultsFile));
//            byte[] results = RabbitMQUtils.writeByteArrays(resultsArray);
//            try {
//
//                sendResultToEvalStorage(taskId, results);
//                System.out.println("Results sent to evaluation storage.");
//            } catch (IOException e) {
//            	System.out.println("Exception while sending storage space cost to evaluation storage." + e.getMessage());
//            }
//        } catch (IOException ex) {
//            java.util.logging.Logger.getLogger(DLinkerSpatialAdapter.class.getName()).log(Level.SEVERE, null, ex);
//        }
//    }
//    
//    public String pythonMatcherController(String source, String target) throws IOException {
//		 System.out.println(source + " -----To Link with---- " + target);
//		 CommandPythonMatcher cpm = new CommandPythonMatcher(source, target);
//		 String result = cpm.runCommand();
//		 System.out.println(result);
//		 this.resultsFile = result;
//		 return result;
//	 }
//
//    @Override
//    public void receiveCommand(byte command, byte[] data) {
//        if (Commands.DATA_GENERATION_FINISHED == command) {
//        	System.out.println("my receiveCommand for source");
//            sourceReceiver.terminate();
//        }
//        super.receiveCommand(command, data);
//    }
//
//    @Override
//    public void close() throws IOException {
//    	System.out.println("Closing System Adapter...");
//        // Always close the super class after yours!
//        super.close();
//        System.out.println("System Adapter closed successfully.");
//    }
}