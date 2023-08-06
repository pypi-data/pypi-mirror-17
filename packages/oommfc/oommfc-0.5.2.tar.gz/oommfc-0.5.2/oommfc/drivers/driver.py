import os
import glob
import oommfodt
import micromagneticmodel as mm
import discretisedfield as df


class Driver(mm.Driver):
    def drive(self, system, **kwargs):
        """
        Drive the system.

        """
        filenames = self._filenames(system)

        # Make directory for saving OOMMF files.
        self._makedir(system)

        # Save system's magnetisation configuration omf file.
        omffilename = filenames["omffilename"]
        system.m.write_oommf_file(omffilename)

        # Save OOMMF configuration mif file.
        miffilename = filenames["miffilename"]
        self._save_mif(system, **kwargs)

        # Run simulation.
        self._run_simulator(system)

        # Update system.
        self._update_system(system)

    def _makedir(self, system):
        """
        Create directory where OOMMF files are saved.
        """
        dirname = self._filenames(system)["dirname"]
        if not os.path.exists(dirname):
            os.makedirs(dirname)

    def _save_mif(self, system, **kwargs):
        """
        Save OOMMF configuration mif file.
        """
        mif = "# MIF 2.1\n\n"
        mif += system.script()
        mif += self.script(system, **kwargs)

        miffilename = self._filenames(system)["miffilename"]
        miffile = open(miffilename, "w")
        miffile.write(mif)
        miffile.close()

    def _run_simulator(self, system):
        dirname = self._filenames(system)["dirname"]
        miffilename = self._filenames(system)["miffilename"]

        if os.name == "nt":
            oommf_command = ("tclsh86 %OOMMFTCL% "  # pragma: no cover
                             "boxsi +fg {} -exitondone 1").format(miffilename)
        else:
            oommf_command = ("tclsh $OOMMFTCL boxsi +fg {} "
                             "-exitondone 1").format(miffilename)
        os.system("cd {}".format(dirname))
        returncode = os.system(oommf_command)
        if returncode:
            raise Exception("Error in running OOMMF")  # pragma: no cover

    def _update_system(self, system):
        self._update_m(system)
        self._update_dt(system)

    def _update_m(self, system):
        # Find last omf file.
        dirname = self._filenames(system)["dirname"]
        last_omf_file = max(glob.iglob("{}*.omf".format(dirname)),
                            key=os.path.getctime)

        # Update system's magnetisaton.
        system.m = df.read_oommf_file(last_omf_file,
                                      normalisedto=system.m.normalisedto)

    def _update_dt(self, system):
        # Find last odt file.
        dirname = self._filenames(system)["dirname"]
        last_odt_file = max(glob.iglob("{}*.odt".format(dirname)),
                            key=os.path.getctime)

        # Update system's datatable.
        system.dt = oommfodt.OOMMFodt(last_odt_file).df

    def _filenames(self, system):
        dirname = "{}/".format(system.name)
        omffilename = "{}m0.omf".format(dirname)
        miffilename = "{}{}.mif".format(dirname, system.name)

        filenames = {}
        filenames["dirname"] = dirname
        filenames["omffilename"] = omffilename
        filenames["miffilename"] = miffilename

        return filenames
