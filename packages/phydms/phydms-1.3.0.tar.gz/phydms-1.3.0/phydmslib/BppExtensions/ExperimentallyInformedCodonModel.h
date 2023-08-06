// 
// File: ExperimentallyInformedCodonModel.h
// Created by: Jesse Bloom
// Created on: May 2015
//

/*
  This file was created by modifying the 
  CodonDistanceFitnessPhaseFrequenciesSubstitutionModel.h file
  distributed with Bio++
*/
 
/*
  Copyright or © or Copr. Bio++ Development Team, (November 16, 2004)

  This software is a computer program whose purpose is to provide classes
  for phylogenetic data analysis.
 
  This software is governed by the CeCILL  license under French law and
  abiding by the rules of distribution of free software.  You can  use,
  modify and/ or redistribute the software under the terms of the CeCILL
  license as circulated by CEA, CNRS and INRIA at the following URL
  "http://www.cecill.info".
 
  As a counterpart to the access to the source code and  rights to copy,
  modify and redistribute granted by the license, users are provided only
  with a limited warranty  and the software's author,  the holder of the
  economic rights,  and the successive licensors  have only  limited
  liability.
 
  In this respect, the user's attention is drawn to the risks associated
  with loading,  using,  modifying and/or developing or reproducing the
  software by the user in light of its specific status of free software,
  that may mean  that it is complicated to manipulate,  and  that  also
  therefore means  that it is reserved for developers  and  experienced
  professionals having in-depth computer knowledge. Users are therefore
  encouraged to load and test the software's suitability as regards their
  requirements in conditions enabling the security of their systems and/or
  data to be ensured and,  more generally, to use and operate it in the
  same conditions as regards security.
 
  The fact that you are presently reading this means that you have had
  knowledge of the CeCILL license and that you accept its terms.
*/
 
#include <Bpp/Phyl/Model/Codon/AbstractCodonSubstitutionModel.h>
#include <Bpp/Phyl/Model/Codon/AbstractCodonPhaseFrequenciesSubstitutionModel.h>
#include <Bpp/Numeric/AbstractParameterAliasable.h>

namespace bppextensions
{
  /**
   * @brief Class for experimentally informed codon substitution model
   *
   * @author Jesse Bloom
   *
   * @param gCode The genetic code
   *
   * @param preferences The preference for the amino acid encoded by each codon
   *
   * @param prefix The name prefixed to the model, such as "ExpCM_residue_1."
   *
   *@param prefsasparams Are the preferences defined as model parameters?
   *
   * @param divpressure 
   *
   * @param divpressure Are site-specific diversifying pressures given? 
   *
   * @param mindeltar The maximum diversifying pressure across all sites
   *
   * @param maxdeltar The minimum diversifying pressure across all sites
   *
   * @param deltar The diversifying pressure
   *
   * @param Method for getting fixation probs from preferences. Can be "HalpernBruno", "FracTolerated", "gwF"
   *
   * References:
   * -  Bloom JD (2016), _bioRxiv_, DOI: 10.1101/037689 (2016)
   * -  Bloom JD (2014), _Molecular Biology and Evolution_ 31(10):2753-2769.
   */
  class ExperimentallyInformedCodonModel :
    public virtual bpp::AbstractParameterAliasable,
    public virtual bpp::ReversibleSubstitutionModel,
    public bpp::AbstractCodonSubstitutionModel,
    public bpp::AbstractCodonPhaseFrequenciesSubstitutionModel
  {
  private:
    std::string prefix_;
    std::string prefName_;
    bpp::FrequenciesSet* preferences_;
    double scaledprefsum_;
    double omega_; // dN/dS ratio
    double omega2_;
    double stringencyparameter_;
    double rateparameter_;
    bool prefsasparams_;
    double deltar_;
    bool divpressure_;
    double f_gwF_;
    std::string fixationmodel_;

  public:
    ExperimentallyInformedCodonModel(
        const bpp::GeneticCode* gCode,
        bpp::FrequenciesSet* preferences, 
        const std::string& prefix,
        bool prefsasparams,
        bool divpressure,
        double maxdeltar,
        double mindeltar,
        double deltar,
        std::string fixationmodel);

    ExperimentallyInformedCodonModel(const ExperimentallyInformedCodonModel& model):
      AbstractParameterAliasable(model),
      AbstractCodonSubstitutionModel(model),
      AbstractCodonPhaseFrequenciesSubstitutionModel(model),
      prefix_(model.prefix_),
      preferences_(model.preferences_->clone()),
      omega_(model.omega_),
      omega2_(model.omega2_),
      stringencyparameter_(model.stringencyparameter_),
      rateparameter_(model.rateparameter_),
      prefsasparams_(model.prefsasparams_),
      deltar_(model.deltar_),
      divpressure_(model.divpressure_),
      f_gwF_(model.f_gwF_),
      fixationmodel_(model.fixationmodel_)
      
    {} 

    ExperimentallyInformedCodonModel& operator=(const ExperimentallyInformedCodonModel& model) {
      AbstractParameterAliasable::operator=(model);
      AbstractCodonSubstitutionModel::operator=(model);
      AbstractCodonPhaseFrequenciesSubstitutionModel::operator=(model);
      prefix_ = model.prefix_;
      if (preferences_) delete preferences_;
      preferences_ = model.preferences_->clone();
      omega_ = model.omega_;
      omega2_ = model.omega2_;
      stringencyparameter_ = model.stringencyparameter_;
      rateparameter_ = model.rateparameter_;
      prefsasparams_ = model.prefsasparams_;
      deltar_ = model.deltar_;
      divpressure_ = model.divpressure_;
      f_gwF_ = model.f_gwF_;
      fixationmodel_ = model.fixationmodel_;
      
      return *this;
    }

    virtual ~ExperimentallyInformedCodonModel();

    ExperimentallyInformedCodonModel* clone() const
    {
      return new ExperimentallyInformedCodonModel(*this);
    }

  public:
    void fireParameterChanged(const bpp::ParameterList& parameterlist);

    std::string getName() const;

    double getCodonsMulRate(size_t i, size_t j) const;

    void setNamespace(const std::string&);

    /*
     * @brief returns the preferences in a map keyed by codon and with value as preferences
     *
     */
    std::map<std::string, double> getPreferences();

    /*
     * @brief gets namespace for preferences
     */
    std::string getPreferencesNamespace();

    /*
     * @brief set the phasefrequencies and fitness of the model from
     * given frequencies, such that the equilibrium frequencies of the
     * model matches at best the given ones.
     * 
     * Matching is done in two steps : first, phase frequencies are
     * matched at best, then the resulting discrepancy (in terms of
     * ratios between the given one and the one computed by the pahse
     * frequencies) is given for matching to the fitness.
     *
     * @ param frequencies  the frequencies to match on.
     */
    void setFreq(std::map<int,double>& frequencies);

  };

} // end of namespace bppextensions.
