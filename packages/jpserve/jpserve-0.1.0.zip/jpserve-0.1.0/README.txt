jpserve
""""""""""""""""""

Jpserve provides a simple and high performance way to execute Python script in JAVA. It includes PyServe and JClient API. 

* PyServe is an execute server running on Python side and listening the execute requests from JAVA.
* The JClient API can executes Python snippet or complete script file from java, it send the script to PyServe and get the execution result. The result is JSON format, so you can exchange the complex data between JAVA and Python flexibly.

Quick Start
""""""""""""""""""

Python Side
------------------

Open Python console, import jpserve and start the PyServe:

>>> from jpserve.jpserve import PyServe
>>> server = PyServe(("localhost", 8888))
>>> server.start()
>>>
    INFO:pserve:starting...
    INFO:pserve:pyserve listening in localhost 8888 
>>>


JAVA Side
------------------
>>>
// init the PyServeContext, it will make a connection to PyServe
PyServeContext.init("localhost", 8888);
// 
// prepare the script, and assign the return value to _result_
String script = "a = 2\n"
              + "b = 3\n"
              + "_result_ = a * b";
//
// sned the script to PyServe, it returns the final result
PyResult rs = executor.exec(s);
//
// check if the execution is success
if (rs.isSuccess()) {
  System.out.println("Result: " + rs.getResult()); // get the _result_ value
}
else {
  System.out.println("Execute python script failed: " + rs.getMsg());
}              
------------------------
Result: 6