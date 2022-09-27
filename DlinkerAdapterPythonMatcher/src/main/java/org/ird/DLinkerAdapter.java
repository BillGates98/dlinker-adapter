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
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.rabbitmq.client.ConsumerCancelledException;
import com.rabbitmq.client.ShutdownSignalException;

public class DLinkerAdapter extends AbstractSystemAdapter {

	private static final Logger LOGGER = LoggerFactory.getLogger(DLinkerAdapter.class);
	private SimpleFileReceiver sourceReceiver;
	private SimpleFileReceiver targetReceiver;
	private String receivedGeneratedDataFilePath;
	private String dataFormat;
	private String taskFormat;
	private String resultsFile;

	@Override
	public void init() throws Exception {
		super.init();

		// Your initialization code comes here...
		System.out.println("initializing times test system...");
		long time = System.currentTimeMillis();

		super.init();

		System.out.println("Super class initialized. it took " + (System.currentTimeMillis()-time) + "ms");

		time = System.currentTimeMillis();

		sourceReceiver = SimpleFileReceiver.create(this.incomingDataQueueFactory, "source_file");
		System.out.println("Receivers initialized. It took " + (System.currentTimeMillis()-time) + "ms");

		System.out.println("DLinker initialized successfully.");
		// You can access the RDF model this.systemParamModel 
		// to retrieve meta data defined in your system.ttl file
	}

	@Override
	public void receiveGeneratedData(byte[] data) {
		// handle the incoming data as described in the benchmark description
		try {
			System.out.println("Starting receiveGeneratedData..");
			ByteBuffer dataBuffer = ByteBuffer.wrap(data);
			dataFormat = RabbitMQUtils.readString(dataBuffer);
			System.out.println("DataFormat : " + dataFormat);
			String absoluteSourcePath = "";
			String[] receivedFiles = sourceReceiver.receiveData("datasets/SourceDatasets/");
			for(String file: receivedFiles) {
				absoluteSourcePath = this.getAbsolutePathofResources("datasets/SourceDatasets/" + file);
				System.out.println("File Received in RGD : " + file);
			}
			receivedGeneratedDataFilePath = absoluteSourcePath;
			System.out.println("Received data from receivedGeneratedData..");

		} catch(IOException | ShutdownSignalException | ConsumerCancelledException | InterruptedException ex) {
			java.util.logging.Logger.getLogger(DLinkerAdapter.class.getName()).log(Level.SEVERE, null, ex);
		} 
	}

	private String getAbsolutePathofResources(String file){
		return new File(file).getAbsolutePath();
	}

	@Override
	public void receiveGeneratedTask(String taskId, byte[] data) {
		// handle the incoming task and create a result
		System.out.println("Starting receiveGeneratedTask..");
		System.out.println("Task " + taskId + " received from task generator");
		long time = System.currentTimeMillis();
		try {
			ByteBuffer taskBuffer = ByteBuffer.wrap(data);
			taskFormat = RabbitMQUtils.readString(taskBuffer);
			System.out.println("TaskFormat : " + dataFormat);
			System.out.println("Parsed task "+ taskId + ". It took " + (System.currentTimeMillis() - time) + "ms");
			time = System.currentTimeMillis();
			String receivedGeneratedTaskFilePath = null;
			try {
				targetReceiver = SingleFileReceiver.create(this.incomingDataQueueFactory, "task_target_file");
				String absoluteTargetPath = null;
				String[] receivedFiles = targetReceiver.receiveData("datasets/TargetDatasets/");
				for(String file: receivedFiles) {
					absoluteTargetPath = this.getAbsolutePathofResources("datasets/TargetDatasets/" + file);
					System.out.println("File Received in RGT : " + absoluteTargetPath);
				}
				receivedGeneratedTaskFilePath = absoluteTargetPath;
			} catch(Exception e) {
				System.out.println("Exception while trying to receive data. Aborting." + e.getMessage());
			}
			System.out.println("Received task data. It took " + (System.currentTimeMillis()-time) + "ms");

			// main program
			if (receivedGeneratedDataFilePath != null && receivedGeneratedTaskFilePath != null) {
				System.out.println("Size of source file " + new File(receivedGeneratedDataFilePath).length());
				System.out.println("Size of target file " + new File(receivedGeneratedTaskFilePath).length());
				resultsFile = pythonMatcherController(receivedGeneratedDataFilePath, receivedGeneratedTaskFilePath);
				if (resultsFile != null && resultsFile.trim().length()>0) {
					byte[][] resultsArrays = new byte[1][];
					String tmpFile = this.getAbsolutePathofResources(resultsFile);
					resultsArrays[0] = FileUtils.readFileToByteArray(new File(tmpFile));
					byte[] results = RabbitMQUtils.writeByteArrays(resultsArrays);
					System.out.println("Results ready for evaluation : " + tmpFile + " with size " + new File(tmpFile).length());
					sendResultToEvalStorage(taskId, results);
					System.out.println("Results sent to evaluation storage successfully");
				} 
			}
		}catch(IOException ex) {
			java.util.logging.Logger.getLogger(DLinkerAdapter.class.getName()).log(Level.SEVERE, null, ex);
		}
	}

	@Override
	public void close() throws IOException {
		// Free the resources you requested here
		System.out.println("Closing system adapter");
		System.out.println("System adapter closed successfully.");
		super.close();
		// Always close the super class after yours!
	}

	public String pythonMatcherController(String source, String target) throws IOException {
		System.out.println(source + " -----To Link with---- " + target);
		CommandPythonMatcher cpm = new CommandPythonMatcher(source, target);
		String result = cpm.runCommand();
		System.out.println("Output file detected : " + result);
		return result;
	}

	@Override
	public void receiveCommand(byte command, byte[] data) {
		if (Commands.DATA_GENERATION_FINISHED == command) {
			System.out.println("my receiveCommand for source");
			sourceReceiver.terminate();
		} else if (Commands.TASK_GENERATION_FINISHED == command) {
			System.out.println("my receiveCommand for target");
			targetReceiver.terminate();
		} else if (Commands.BENCHMARK_FINISHED_SIGNAL == command) {
			System.out.println("End signal so early ended");
		}
		super.receiveCommand(command, data);
	}

}