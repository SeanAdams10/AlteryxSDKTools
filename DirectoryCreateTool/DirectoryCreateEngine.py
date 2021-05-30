"""
AyxPlugin (required) has-a IncomingInterface (optional).
Although defining IncomingInterface is optional, the interface methods are needed if an upstream tool exists.
"""


import os, sys
os.environ['PATH'] = r'C:\program files\Alteryx\bin;' + os.environ['PATH']
sys.path.insert(1, r'C:\program files\Alteryx\bin\plugins')
import AlteryxPythonSDK

import AlteryxPythonSDK as Sdk
import xml.etree.ElementTree as Et
import os





class AyxPlugin:
    """
    Implements the plugin interface methods, to be utilized by the Alteryx engine to communicate with a plugin.
    Prefixed with "pi", the Alteryx engine will expect the below five interface methods to be defined.
    """


    def __init__(self, n_tool_id: int, alteryx_engine: object, output_anchor_mgr: object):
        """
        Constructor is called whenever the Alteryx engine wants to instantiate an instance of this plugin.
        :param n_tool_id: The assigned unique identification for a tool instance.
        :param alteryx_engine: Provides an interface into the Alteryx engine.
        :param output_anchor_mgr: A helper that wraps the outgoing connections for a plugin.

        https://help.alteryx.com/developer/current/Python/use/AyxPluginClass.htm#__init__
        This is the standard Python constructor, which is called each time the Alteryx Engine instantiates an instance of your plugin.
        __init__(self, n_tool_id, alteryx_engine, output_anchor_mgr)
        The arguments to this function are values provided by the Alteryx Engine, and will be used when communicating with the engine or with other tools.
        n_tool_id: An integer representing a unique identifier for the instance of the tool being created. Your plugin should save this value to communicate with the Alteryx Engine.
        alteryx_engine: A complex object representing the interface for communicating with the Alteryx Engine.
        output_anchor_mgr: A complex object used to interface with the output connections of your tool. You need to call get_output_anchor on it with the name of your output in the config file to get the handle for the output.
        """

        # Default properties
        self.n_tool_id = n_tool_id
        self.alteryx_engine = alteryx_engine
        self.output_anchor_mgr = output_anchor_mgr

        # Custom properties
        self.is_initialized = True
        self.single_input = None
        self.rootFolderField = None
        self.targetFolderField = None
        self.record_info_inbound = None
        self.record_info_outbound = None
        
        
    def pi_init(self, str_xml: str):
        """
        Called when the Alteryx engine is ready to provide the tool configuration from the GUI.
        :param str_xml: The raw XML from the GUI.

        https://help.alteryx.com/developer/current/Python/use/AyxPluginClass.htm#pi_init
        Provides the tool with its configuration data. Required method.
        pi_init(self, str_xml)
        str_xml: A string formatted as XML that holds the config data.
        This function is called when the tool is first initialized and any time the tool configuration changes.
        """

        # Getting the user-entered selections from the GUI.
        if Et.fromstring(str_xml).find('rootFolderFieldSelect') is not None:
            self.rootFolderField = Et.fromstring(str_xml).find('rootFolderFieldSelect').text
        if Et.fromstring(str_xml).find('targetFolderFieldSelect') is not None:
            self.targetFolderField = Et.fromstring(str_xml).find('targetFolderFieldSelect').text


        # Letting the user know of the necessary selections, if they haven't been selected.
        if self.rootFolderField is None:
            self.alteryx_engine.output_message(self.n_tool_id, Sdk.EngineMessageType.error, 'Please select the root folder field')
        if self.targetFolderField is None:
            self.alteryx_engine.output_message(self.n_tool_id, Sdk.EngineMessageType.error, 'Please select the target folder field')

        self.output_anchor = self.output_anchor_mgr.get_output_anchor('result')  # Getting the output anchor from the XML file.

        





    def pi_close(self, b_has_errors: bool):
        """
        Called after all records have been processed..
        :param b_has_errors: Set to true to not do the final processing.
            
        https://help.alteryx.com/developer/current/Python/use/AyxPluginClass.htm#pi_close
        Required method.
        pi_close(self, b_has_errors)
        b_has_errors: An option the indicates if errors occurred. 
        Use pi_close() if you require file cleanup that must handled manually or to issue an error that cannot be detected before pi_close.
        """
    
        self.alteryx_engine.output_message(self.n_tool_id, Sdk.EngineMessageType.info, self.xmsg('Method: pi_close: starting'))

        self.output_anchor.assert_close()  # Checks whether connections were properly closed.
        

    def pi_add_incoming_connection(self, str_type: str, str_name: str) -> object:
        """
        The IncomingInterface objects are instantiated here, one object per incoming connection.
        Called when the Alteryx engine is attempting to add an incoming data connection.
        :param str_type: The name of the input connection anchor, defined in the Config.xml file.
        :param str_name: The name of the wire, defined by the workflow author.
        :return: The IncomingInterface object(s).

        https://help.alteryx.com/developer/current/Python/use/AyxPluginClass.htm#pi_add_i
        Manages input data, metadata, and progress for one or more incoming connections.
        pi_add_incoming_connection(self, str_type, str_name)
        Returns an object that implements the incoming interface functions.

        """
    
        self.single_input = IncomingInterface(self) #Store this for later.    This code triggers the constructor for ii
        return self.single_input
    

    def pi_add_outgoing_connection(self, str_name: str) -> bool:
        """
        Called when the Alteryx engine is attempting to add an outgoing data connection.
        :param str_name: The name of the output connection anchor, defined in the Config.xml file.
        :return: True signifies that the connection is accepted.

        https://help.alteryx.com/developer/current/Python/use/AyxPluginClass.htm#pi_add_o
        Passes output anchor and related connections.
        pi_add_outgoing_connection(self, str_name)

        """

        return True


    def pi_push_all_records(self, n_record_limit: int) -> bool:
        """
        Called when a tool has no incoming data connection.
        :param n_record_limit: Set it to <0 for no limit, 0 for no records, and >0 to specify the number of records.
        :return: True for success, False for failure.

        https://help.alteryx.com/developer/current/Python/use/AyxPluginClass.htm#pi_push_
        Called for tools that do not have inputs.
        pi_push_all_records(self, n_record_limit)
        """

        if not self.is_initialized:
            return False

        n_record_limit = 99999
        return true

    
    def xmsg(self, msg_string: str) -> str:
        """
        A non-interface, non-operational placeholder for the eventual localization of predefined user-facing strings.
        :param msg_string: The user-facing string.
        :return: msg_string
        """

        return msg_string



class IncomingInterface:
    """
    This optional class is returned by pi_add_incoming_connection, and it implements the incoming interface methods, to
    be utilized by the Alteryx engine to communicate with a plugin when processing an incoming connection.
    Prefixed with "ii", the Alteryx engine will expect the below four interface methods to be defined.
    """

    def __init__(self, parent: object):
        """
        Constructor for IncomingInterface.
        :param parent: AyxPlugin

        """
 
        # Default properties
        self.parent = parent

        #Custom properties
        self.record_info_inbound = None #holds the record info object for the inbound data stream
        self.record_info_out = None  #holds the record info object for the outbound side of the data stream
        self.record_copier = None #do we need to store our own record copier?
        self.record_creator = None #do we need to store our own record creator?
        self.fldCreationResult = None #store the field reference for the first field added to the ouput.  Gives a status on the field creation
        self.fldCreationDescr = None  #store the field reference for the second field added to the ouput.  Gives a detiled message on the field creation e.g. error messages

        

    def ii_init(self, record_info_in: object) -> bool:
        """
        Called to report changes of the incoming connection's record metadata to the Alteryx engine.
        :param record_info_in: A RecordInfo object for the incoming connection's fields.
        :return: True for success, otherwise False.

        https://help.alteryx.com/developer/current/Python/use/AyxPluginClass.htm#ii_init
        ii_init(self, record_info_in)
        record_info_in: The incoming record structure.
        """

        #standard pieces
        self.parent.record_info_inbound = record_info_in
        self.record_info_inbound = record_info_in

        #Set up the outbound record structure
        self.record_info_out = self.record_info_inbound.clone()
        
        self.fldCreationResult = self.record_info_out.add_field(
                field_name= 'FolderCreationResult', 
                field_type=Sdk.FieldType.v_wstring, 
                size=200, 
                source='DirectoryCreate Tool - ID: ' + str(self.parent.n_tool_id), 
                description='Result of folder creation') 

        self.fldCreationDescr = self.record_info_out.add_field(
                field_name= 'FolderCreationDescription', 
                field_type=Sdk.FieldType.v_wstring, 
                size=200, 
                source='DirectoryCreate Tool - ID: ' + str(self.parent.n_tool_id), 
                description='Detailed status / error message for folder creation')

        self.fldRootFolder = self.record_info_out[self.record_info_out.get_field_num(self.parent.rootFolderField)]
        self.fldTargetFolder = self.record_info_out[self.record_info_out.get_field_num(self.parent.targetFolderField)]
        

        #Assign this recordInfo and recordset to the outbound anchor
        self.parent.output_anchor.init(self.record_info_out)  # Lets the downstream tools know what the outgoing record metadata will look like, based on record_info_out.


        #Create a record Creator, from the new recordInfo structure
        self.record_creator = self.record_info_out.construct_record_creator()
        #Then create a record copier
        self.record_copier = Sdk.RecordCopier(self.record_info_out, self.record_info_inbound)
		# Map each column of the input to where we want in the output - for the inbound fields - still have to do the 2 additional fields later
        for index in range(self.record_info_inbound.num_fields):
			# Adding a field index mapping.
            self.record_copier.add(index, index)
        self.record_copier.done_adding()

        return True

    def ii_push_record(self, in_record: object) -> bool:
        """
        Responsible for pushing records out.
        Called when an input record is being sent to the plugin.
        :param in_record: The data for the incoming record.
        :return: true if this record should be pushed.

        https://help.alteryx.com/developer/current/Python/use/AyxPluginClass.htm#ii_push_
        Pushes records downstream. If your tool processes a single record at a time, it is best to push the record downstream from within the tool.
        ii_push_record(self, in_record)
        Return False to indicate that no additional records are required.

        """
        #Reset the record creator and record copier to copy the fields that are staying the same
        self.record_creator.reset()
        self.record_copier.copy(self.record_creator, in_record)

        strThisRowRootFolder = self.fldRootFolder.get_as_string(in_record)
        strThisRowTargetFolder = self.fldTargetFolder.get_as_string(in_record)

        result,message = self.createFolder(strThisRowRootFolder,strThisRowTargetFolder)


        self.fldCreationResult.set_from_string(self.record_creator,result)
        self.fldCreationDescr.set_from_string(self.record_creator,message)

        out_record = self.record_creator.finalize_record()

        self.parent.output_anchor.push_record(out_record)
        self.parent.output_anchor.output_record_count(False)
        return True
    

    def ii_update_progress(self, d_percent: float):
        """
        Called by the upstream tool to report what percentage of records have been pushed.
        :param d_percent: Value between 0.0 and 1.0.

        https://help.alteryx.com/developer/current/Python/use/AyxPluginClass.htm#ii_updat
        Updates the upstream tool of record-processing progress.
        ii_update_progress(self, d_percent)

        """

        self.parent.alteryx_engine.output_tool_progress(self.parent.n_tool_id, d_percent)  # Inform the Alteryx engine of the tool's progress.
        self.parent.output_anchor.update_progress(d_percent)  # Inform the downstream tool of this tool's progress.
        
    def ii_close(self):
        """
        Called when the incoming connection has finished passing all of its records.
        
        https://help.alteryx.com/developer/current/Python/use/AyxPluginClass.htm#ii_close
        Closes connection to upstream tool when all records have been pushed, indicated by upstream tool calling self.output_anchor.close(). 
        Close all resources opened in ii_init.
        ii_close(self)
        """

        self.parent.output_anchor.output_record_count(True)  # True: Let Alteryx engine know that all records have been sent downstream.
        self.parent.output_anchor.close()  # Close outgoing connections.



    def createFolder(self, rootFolder:str, targetFolder: str):
        #Function to do the actual directory creation
        import os
    
        # validate if the root folder exists
        if not(os.path.isdir(rootFolder)):
            result = 'False'
            message = "Root folder {} does not exist".format(rootFolder)
            return result, message

        # Create the sub-folder
        if os.path.isdir(targetFolder):
            #folder already exists
            result = 'True'
            message = 'Folder already existed'
        else:
            try:
                os.makedirs(targetFolder)
            except:
                result = 'False'
                message = 'Error while creating folder'
            else:
                result = 'True'
                message = 'Created Successfully'
        return result, message


