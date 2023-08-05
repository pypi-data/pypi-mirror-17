
name := "py4jdbc"

version := "0.1.6.8"

scalaSource in Compile := baseDirectory.value / "src"

libraryDependencies ++= Seq(
    "net.sf.py4j" % "py4j" % "0.9",
    "org.spark-project" % "pyrolite" % "2.0",
    "org.apache.derby" % "derby" % "10.9.1.0",
    "postgresql" % "postgresql" % "9.1-901-1.jdbc4"
    )

